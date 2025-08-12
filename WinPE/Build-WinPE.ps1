<# 
.DESCRIPTION
  - Creates WinPE working directory (copype)
  - Mounts boot.wim
  - Injects drivers
  - Adds WinPE packages
  - Copies custom scripts & 3rd-party apps
  - Customizes startnet.cmd
  - Builds ISO or USB

.PARAMETER Config
  Path to JSON configuration.

.NOTES
  Run as Administrator.
#>

[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)]
  [string]$ConfigPath
)

function Check-Admin {
  $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
  ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
  if (-not $isAdmin) { throw "Please run this script as Administrator." }
}

Check-Admin

# === Load config ===
if (-not (Test-Path $ConfigPath)) { throw "Config not found: $ConfigPath" }
$cfg = Get-Content -Raw -Path $ConfigPath | ConvertFrom-Json

$arch = $cfg.architecture
$root = $cfg.projectRoot
$out = $cfg.output

# Common paths
$adkRoot = "${env:ProgramFiles(x86)}\Windows Kits\10\Assessment and Deployment Kit"
$peAddon = Join-Path $adkRoot "Windows Preinstallation Environment"
$ocsRoot = Join-Path $peAddon "$arch\WinPE_OCs"
$work    = Join-Path $root "Work"
$mount   = Join-Path $root "Mount"
$media   = Join-Path $work "Media"
$bootWim = Join-Path $media "media\sources\boot.wim"

New-Item -ItemType Directory -Force -Path $root,$work,$mount | Out-Null
if (Test-Path $media) { Remove-Item -Recurse -Force $media }

# Create WinPE working dir
# $copype = Join-Path $peAddon "copype.cmd"
$DandISetEnv = Join-Path $adkRoot "Deployment Tools\DandISetEnv.bat"
cmd /c "`"$DandISetEnv`" && copype $arch $media"
if ($LASTEXITCODE -ne 0) { throw "copype failed" }

# Mount image
Dism /Mount-Image /ImageFile:$bootWim /Index:1 /MountDir:$mount
if ($LASTEXITCODE -ne 0) { throw "Mount failed" }

try {
  # Drivers
  foreach ($dir in ($cfg.drivers | ForEach-Object { $_ })) {
    if (Test-Path $dir) { dism /Image:$mount /Add-Driver /Driver:$dir /Recurse }
  }

  # Packages (WinPE optional components)
  foreach ($p in ($cfg.packages | ForEach-Object { $_ })) {
    $cab = if (Test-Path $p) { $p } else { Get-ChildItem -Path $ocsRoot -Filter $p -ErrorAction SilentlyContinue | Select-Object -First 1 | ForEach-Object FullName }
    if ($cab) { dism /Image:$mount /Add-Package /PackagePath:$cab }
  }

  # Copy files
  foreach ($f in ($cfg.copyScripts | ForEach-Object { $_ })) {
    $dst = Join-Path $mount ($f.Dest.TrimStart('\'))
    New-Item -ItemType Directory -Force -Path (Split-Path $dst -Parent) | Out-Null
    Copy-Item -Force -Path $f.Source -Destination $dst
  }

  # Copy folders
  foreach ($d in ($cfg.apps | ForEach-Object { $_ })) {
    $dst = Join-Path $mount ($d.Dest.TrimStart('\'))
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    Copy-Item -Recurse -Force -Path $d.Source -Destination $dst
  }

  # startnet.cmd
  if ($cfg.startnet -and $cfg.startnet.Count -gt 0) {
    $sn = Join-Path $mount "Windows\System32\startnet.cmd"
    if (-not (Test-Path $sn)) { "wpeinit" | Set-Content -Encoding ASCII -Path $sn }
    $current = Get-Content -Path $sn -ErrorAction SilentlyContinue
    if (-not ($current -match '^\s*wpeinit\s*$')) { "wpeinit`r`n$($current -join "`r`n")" | Set-Content -Encoding ASCII -Path $sn }
    foreach ($line in $cfg.startnet) { Add-Content -Encoding ASCII -Path $sn -Value $line }
  }
}
catch {
  Write-Host "Error: $($_.Exception.Message)"
  dism /Unmount-Image /MountDir:$mount /Discard | Out-Null
  throw
}

# Commit & unmount
Write-Host "Commit Changes and Unmount"
dism /Unmount-Image /MountDir:$mount /Commit
if ($LASTEXITCODE -ne 0) { throw "Commit/Unmount failed" }

# Output (ISO or USB)
switch ($out.type.ToLower()) {
  "iso" {
    $iso = $out.isoPath
    New-Item -ItemType Directory -Force -Path (Split-Path $iso -Parent) | Out-Null
    $DandISetEnv = Join-Path $adkRoot "Deployment Tools\DandISetEnv.bat"
    cmd /c "`"$DandISetEnv`" && MakeWinPEMedia /ISO `"$media`" `"$iso`""
    Write-Host "ISO created: $iso"
  }
  "usb" {
    if (-not $out.usbDriveLetter) { throw "Set output.usbDriveLetter (e.g., 'E:')" }
    $DandISetEnv = Join-Path $adkRoot "Deployment Tools\DandISetEnv.bat"
    cmd /c "`"$DandISetEnv`" && MakeWinPEMedia /UFD `"$media`" `"$($out.usbDriveLetter)`""
    Write-Host "USB created on $($out.usbDriveLetter)"
  }
  default { throw "output.type must be 'iso' or 'usb'" }
}
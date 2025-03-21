from jinja2 import Template

name = "dev01"
osType = "Ubuntu"
isoPath = "C:\\Users\\tamhi\\Documents\\Linux_server_unpack\\ubuntu-server-installer.iso"


  
File = open('powershell_script.temp', 'r') 
content = File.read() 
File.close() 
  
template = Template(content) 
rendered_form = template.render(
    vmname=name, 
    isofile=isoPath,
    cpu=8,
    ram=8192,
    diskSize=40960,
    vmpath="H:\\VMs\\VBOX"
    ) 
  
  
output = open('vbox_build.ps1', 'w') 
output.write(rendered_form)
output.close()
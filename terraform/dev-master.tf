locals {
  size = {
    "small" = {
      cores   = 2
      memory  = 2048
      disk    = "20G"
    }
    "medium" = {
      cores   = 4
      memory  = 4096
      disk    = "40G"
    }
    "large" = {
      cores   = 4
      memory  = 8192
      disk    = "80G"
    }
  }
}

variable "vm_name" {type = string}
variable "vm_size" {type = string}
variable "vmid" {type = number}

resource "proxmox_vm_qemu" "new_vm" {
    name = var.vm_name
    vmid = var.vmid
    target_node = "pve"
    cores = local.size[var.vm_size].cores
    sockets = 1
    cpu_type = "host"
    memory = local.size[var.vm_size].memory
    vm_state = "running"
    scsihw = "virtio-scsi-single"
    agent = 1
    clone = "vm-image"
    onboot = true

    network {
        id = 0
        model    = "virtio"
        bridge   = "vmbr0"
        firewall = true
    }
    # disks {
    #     ide {
    #         ide2 {
    #             cdrom {
    #                 iso = "local:iso/ubuntu-server-installer.iso"
    #             }
    #         }
    #     }
    #     scsi {
    #         scsi2 {
    #             disk {
    #                 size = local.size[var.vm_size].disk
    #                 storage = "local-lvm"
    #             }
    #         }
    #     }
    # }
    disk {
      slot = "scsi0"
      storage = "local-lvm"
      size = local.size[var.vm_size].disk
      backup = false
    }
    os_type = "ubuntu"
}
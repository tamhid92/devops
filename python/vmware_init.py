from jinja2 import Template
import argparse
import os, sys
sys.path.append("../lib")
from hvac_lib import HVACClient
import vm_lib as vm_lib

#Pass node name as an arg
parser = argparse.ArgumentParser(description ='VMWare VM Name')
parser.add_argument('node_name', type=str, help="Node Name")
args = parser.parse_args()

def get_password(account_name):
    vault_client = HVACClient()
    creds =  vault_client.read(f'secret/data/{account_name}')
    for key, value in creds.items():
        username = key
        pwd = value
    return [username, pwd]

def get_vm_info():
    vm_info = {}
    vm_acc = get_password('vmware_rest')
    vm_lib.authenticate(vm_acc[0],vm_acc[1])
    vms = vm_lib.get_vms()
    for vm in vms:
        if vm['path'].split("\\")[-1].split(".")[0] == args.node_name:
            vm_info = {
                "id"    : vm['id'],
                "name"  : vm['path'].split("\\")[-1].split(".")[0]
            }
    return vm_info

def crete_from_template(ip, sudo_pwd):
    with open("../templates/hosts.temp",'r') as file:
        content = file.read()
    template = Template(content) 
    rendered_form = template.render(
        ip_addr=ip,
        sudo_pass=sudo_pwd
    )
    with open("hosts.ini",'w') as file:
        file.write(rendered_form)

def main():
    vm_info = get_vm_info()
    state = vm_lib.get_power(vm_info["id"])
    if state["power_state"] == 'poweredOff':
        print("VM powered off, turning on...")
        vm_lib.update_power(vm_info["id"], 'on')
        print("Waiting for VM to start...sleeping for 30 seconds")
        time.sleep(30)
        print(vm_lib.get_power(vm_info["id"]))
    else:
        print("VM already running...")
    
    ip = vm_lib.get_ip(vm_info["id"])
    crete_from_template((vm_lib.get_ip(vm_info["id"])["ip"]), get_password('sudo')[1])

main()
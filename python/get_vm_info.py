import vm_rest_lib
import argparse
import os

parser = argparse.ArgumentParser(description ='VMWare VM Name')
uname = os.environ.get("api_user")
pwd = os.environ.get("api_pass")
parser.add_argument('node_name', type=str, help="Node Name")
args = parser.parse_args()

def get_vm_info(resp, node_name):
    vm_info = {}
    for vm in resp:
        if vm['path'].split("\\")[-1].split(".")[0] == node_name:
            ip_resp = vm_rest_lib.get_ip(vm['id'])
            vm_info = {
                "id"    : vm['id'],
                "name"  : vm['path'].split("\\")[-1].split(".")[0],
                "ip"    : ip_resp['ip']
            }
    print(vm_info)
    return vm_info

def generate_inv_file(ip_addr):
    ini_data = f"""
[master]
{ip_addr}

[master:vars]
ansible_ssh_private_key_file=/home/tamhid/keys/tamhid_key
    """
    print(ip_addr)
    return ini_data

def main():

    vm_rest_lib.authenticate(uname, pwd)
    vms = vm_rest_lib.get_vms()
    vm_info = get_vm_info(vms, args.node_name)
    
    ini_data = generate_inv_file(vm_info['ip'])
    with open("../ansible/hosts.ini", "w+") as file:
        file.write(ini_data)

if __name__ == '__main__':
    main()
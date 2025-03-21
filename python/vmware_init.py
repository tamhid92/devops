from hvac_lib import HVACClient
import vm_rest_lib
import argparse
import os

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

def main():
    pwd = get_password('postgres')

main()
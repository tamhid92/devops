import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
api_base = f'https://192.168.68.79:8006'
print(f'Proxmox API base URL: {api_base}')

# Proxmox API token
PROXMOX_TOKEN_NAME = "root@pam!terraform"
PROXMOX_TOKEN_VALUE = "942f20a3-d87d-4f3a-9aba-402c05583a02"

def get_online_node():
    """Fetches the first online node."""
    headers = {
        "Authorization": f"PVEAPIToken={PROXMOX_TOKEN_NAME}={PROXMOX_TOKEN_VALUE}"
    }

    req_url = "/api2/json/nodes/pve/qemu/101/config"

    response = requests.get(f"{api_base}{req_url}", headers=headers, verify=False)
    if response.status_code != 200:
        print("Failed to fetch nodes:", response.text)
        return None

    # json_data = response.json()
    print(response.text)
    

def main():
    get_online_node()

main()
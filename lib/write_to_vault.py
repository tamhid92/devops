from hvac_lib import HVACClient

vault_client = HVACClient()

CERT_PATH = "/home/ubuntu/.ssh/id_ecdsa"
with open(CERT_PATH, "r") as file:
    cert_data = file.read()
vault_client.write("id_ecdsa", {"id_ecdsa": cert_data})

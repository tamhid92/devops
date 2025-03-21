from hvac_lib import HVACClient
import os

# try:
#     vault_client = HVACClient()

#     secret_data = vault_client.read("secret/data/my_secret")
#     if secret_data:
#         print(f"Secret data: {secret_data}")
#     else:
#         print("Secret not found")

#     data_to_write = {"value": "my_new_secret"}
#     vault_client.write("secret/data/my_new_secret", data_to_write)

#     keys = vault_client.list("secret/data")
#     if keys:
#       print(f"Keys: {keys}")

# except ValueError as e:
#     print(f"Error: {e}")

# if vault_client.is_authenticated():
#   print("Vault client is authenticated")
# else:
#   print("Vault client is not authenticated")


cred = {"tamhid" : "domin8or"}

vault_client = HVACClient()
output =  vault_client.write('ws_creds', cred)
print(output)
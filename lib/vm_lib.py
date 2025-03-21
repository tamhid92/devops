import requests
import json
import base64

class server_params():
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = "8697"
        self.base_url = f"http://{self.ip}:{self.port}/api"

        self.headers = {"Authorization": ("Basic %s" % ""), "Content-type": "application/vnd.vmware.vmw.rest-v1+json", "Accept": "application/vnd.vmware.vmw.rest-v1+json"}

sp = server_params()

def check_response(response):
    if response.status_code == 401:
        print("Server returned unauthenticated error")
    elif response.status_code == 200:
        pass
    elif response.status_code == 204:
        return {}
    elif response.status_code == 404:
        print("Request returned 404")
        return response.content
    else:
        print("Unknown status %d for request" % response.status_code)
    if response.content:
        return json.loads(response.content.decode("ascii"))
    else:
        return {}


def authenticate(username, password):
    authentication_string = base64.b64encode((username + ":" + password).encode('ascii'))
    sp.headers["Authorization"] = ("Basic %s" % authentication_string.decode('ascii'))
    
    response = requests.get(sp.base_url + "/vms", \
        headers=sp.headers)
    check_response(response)
    return response.status_code

def get_vms():

    response = requests.get(sp.base_url + "/vms", \
        headers=sp.headers)
    return check_response(response)

def get_ip(vm_id):

    response = requests.get(sp.base_url + "/vms/" + vm_id + "/ip", \
        headers=sp.headers)
    return check_response(response)

def get_power(vm_id):

    response = requests.get(sp.base_url + "/vms/" + vm_id + "/power", \
        headers=sp.headers)
    return check_response(response)

def update_power(vm_id, params):

    response = requests.put(sp.base_url + "/vms/" + vm_id + "/power", \
        headers=sp.headers, data=params)
    return check_response(response)
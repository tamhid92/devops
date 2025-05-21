import paramiko
import json, psycopg2, io, argparse
from hvac_lib import HVACClient


def get_running_vms_qemu_agent(proxmox_host, proxmox_user, proxmox_key):

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(proxmox_host, username=proxmox_user, key_filename=proxmox_key)

        command = "qm list | awk '{print $1 "  " $2}' | tail -n +2"
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            print(f"Error executing command: {error}")
            return None

        vm_list = output.split("\n")
        vms_temp=[]
        for vm in vm_list:
            if len(vm) >= 2 and 'image' not in vm[3:]:
                vms_temp.append({"vmid": vm[:3], "name": vm[3:]})
        
        all_vms=[]
        for vm in vms_temp:
            command = f"""
                qm guest cmd {vm["vmid"]} network-get-interfaces | jq  '.[1] | ."ip-addresses" | .[0] | ."ip-address"' | tr -d '"'
            """
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            all_vms.append({"vmid": vm["vmid"], "name": vm["name"], "ip_address": output.join(output.split())})

        if error:
            print(f"Error executing command: {error}")
            return None
        
        return all_vms

    except paramiko.AuthenticationException:
        print("Authentication failed.")
        return None
    except paramiko.SSHException as e:
        print(f"SSH error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if ssh:
          ssh.close()

def get_db_connection():

    db_user, db_pass = get_vault('secret/data/postgres')
    
    try:
        conn = psycopg2.connect(
            host="192.168.68.86",
            port=32262,
            database="postgres",
            user=db_user,
            password=db_pass
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def get_vault(path):
    try:
        vault_client = HVACClient()
        db_creds = vault_client.read(path)
        for k,v in db_creds.items():
            user = k
            pwd = v
    except:
        print("Unable to connect to vault")
    return user, pwd

def populate_db(data):
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS VMS (
            vmid INT PRIMARY KEY,
            name VARCHAR(255),
            ip_addr VARCHAR(255)
            );
        """)
        if data:
                cur.executemany("""
                INSERT INTO VMS (vmid, name, ip_addr)
                VALUES (%(vmid)s, %(name)s, %(ip_address)s)
                ON CONFLICT (vmid) DO NOTHING;
            """, data)
        cur.close()
        conn.commit()
        conn.close()
    else:
        print("Database connection failed.")

def main():

    parser = argparse.ArgumentParser(description="Select the ssh key to use for Proxmox")
    parser.add_argument(
        "--ssh-key",
        dest="ssh_key_path",
        required=True,
        help="Path to the SSH private key file.",
    )
    args = parser.parse_args()

    ssh_key_file = args.ssh_key_path
    print(f"SSH key file path provided: {ssh_key_file}")

    proxmox_host = "192.168.68.79"
    proxmox_user = "root"
    proxmox_key = ssh_key_file
    running_vms = get_running_vms_qemu_agent(proxmox_host, proxmox_user, proxmox_key)

    populate_db(running_vms)

if __name__ == '__main__':
    main()
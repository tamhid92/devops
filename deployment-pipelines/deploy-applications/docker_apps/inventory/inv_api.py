from flask import Flask, jsonify, request
import psycopg2, json
from hvac_lib import HVACClient

app = Flask(__name__)

def get_db_connection():
    try:
        db_user, db_pass = get_vault('secret/data/postgres')
        conn = psycopg2.connect(
            host="192.168.68.62",
            port=30727,
            database="postgres",
            user=db_user,
            password=db_pass
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def get_vault(vault_path):
    try:
        vault_client = HVACClient()
        db_creds = vault_client.read(vault_path)
        for k,v in db_creds.items():
            user = k
            pwd = v
        
        return user, pwd
    except:
        print("Unable to get value from Vault")

@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        data = "List of all VMs deployed in Proxmox"
        return data

@app.route('/vms', methods=['GET'])
def get_vms():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT vmid, name, ip_addr FROM vms')
    vms = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'vmid': vm[0], 'name': vm[1], 'ip_addr': vm[2]} for vm in vms])

@app.route('/vms/<string:name>', methods=['GET'])
def get_vm(name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT vmid, name, ip_addr FROM vms WHERE name = %s', (name,))
    vm = cur.fetchone()
    cur.close()
    conn.close()
    if vm:
        return jsonify({'vmid': vm[0], 'name': vm[1], 'ip_addr': vm[2]})
    return jsonify({'error': 'VM not found'}), 404

@app.route('/vms', methods=['POST'])
def create_vm():
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO vms (vmid, name, ip_addr) VALUES (%s, %s, %s)', 
                (data['vmid'], data['name'], data['ip_addr']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'VM added successfully'}), 201

@app.route('/vms/<string:name>', methods=['DELETE'])
def delete_vm(name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM vms WHERE name = %s', (name,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'VM deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
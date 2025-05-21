from flask import Flask, jsonify, request
import psycopg2, json
from hvac_lib import HVACClient
from prometheus_client import generate_latest, Counter, Histogram, Summary
from prometheus_client import CONTENT_TYPE_LATEST
import time


app = Flask(__name__)

# Track number of HTTP requests by method and endpoint
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method'])
# Track request latency in seconds
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency')

def get_db_connection():
    try:
        db_user, db_pass = get_vault('secret/data/postgres')
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
    start_time = time.time()
    REQUEST_COUNT.labels(method='GET').inc()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT vmid, name, ip_addr FROM vms')
    vms = cur.fetchall()
    cur.close()
    conn.close()

    duration = time.time() - start_time
    REQUEST_LATENCY.observe(duration)

    return jsonify([{'vmid': vm[0], 'name': vm[1], 'ip_addr': vm[2]} for vm in vms])

@app.route('/vms/<string:name>', methods=['GET'])
def get_vm(name):

    start_time = time.time()
    REQUEST_COUNT.labels(method='GET').inc()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT vmid, name, ip_addr FROM vms WHERE name = %s', (name,))
    vm = cur.fetchone()
    cur.close()
    conn.close()

    duration = time.time() - start_time
    REQUEST_LATENCY.observe(duration)
    
    if vm:
        return jsonify({'vmid': vm[0], 'name': vm[1], 'ip_addr': vm[2]})
    return jsonify({'error': 'VM not found'}), 404

    

@app.route('/vms', methods=['POST'])
def create_vm():

    start_time = time.time()
    REQUEST_COUNT.labels(method='POST').inc()

    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO vms (vmid, name, ip_addr) VALUES (%s, %s, %s)', 
                (data['vmid'], data['name'], data['ip_addr']))
    conn.commit()
    cur.close()
    conn.close()

    duration = time.time() - start_time
    REQUEST_LATENCY.observe(duration)

    return jsonify({'message': 'VM added successfully'}), 201

@app.route('/vms/<string:name>', methods=['DELETE'])
def delete_vm(name):

    start_time = time.time()
    REQUEST_COUNT.labels(method='DELETE').inc()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM vms WHERE name = %s', (name,))
    conn.commit()
    cur.close()
    conn.close()

    duration = time.time() - start_time
    REQUEST_LATENCY.observe(duration)

    return jsonify({'message': 'VM deleted successfully'})

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
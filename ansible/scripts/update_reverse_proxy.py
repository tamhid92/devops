import sqlite3
import datetime
import os, argparse
from jinja2 import Environment, FileSystemLoader

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", required=True, type=str)
parser.add_argument("-p", "--port", required=True, type=int)
parser.add_argument("-ip","--ipaddress", type=str, default="192.168.68.62")

args = parser.parse_args()
app_name = args.name
app_port = args.port
ip_address = args.ipaddress


BASE_DIR = "/home/ubuntu/ansible"
DB_PATH = os.path.join(BASE_DIR, "database.sqlite")
JSON_PATH = os.path.join(BASE_DIR, "app_vars.json")
TEMPLATE_PATH = os.path.join(BASE_DIR, "ngnix-conf.conf.j2")
NGNIX_FILE_PATH = "/home/ubuntu/ngnix/data/nginx/proxy_host"

def deploy_app():

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Get the latest ID from the database
        cursor.execute("SELECT id FROM proxy_host ORDER BY id DESC LIMIT 1")
        last_record = cursor.fetchone()
        id_ = last_record[0] + 1 if last_record else 1

        today = datetime.datetime.today().replace(microsecond=0)

        sql_data = (
            id_, str(today), str(today), '1', '0',
            f'''["{app_name}.tchowdhury.org"]''',
            ip_address, app_port, '0', '5', '1', '0', '1', '',
            '{"letsencrypt_agree":false,"dns_challenge":false,"nginx_online":true,"nginx_err":null}',
            '0', '1', 'http', '1', '[]', '0', '0'
        )

        insert_sql = """
            INSERT INTO proxy_host
            (id, created_on, modified_on, owner_user_id, is_deleted, domain_names, 
            forward_host, forward_port, access_list_id, certificate_id, ssl_forced, 
            caching_enabled, block_exploits, advanced_config, meta, allow_websocket_upgrade, 
            http2_support, forward_scheme, enabled, locations, hsts_enabled, hsts_subdomains)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (id) DO NOTHING
        """

        cursor.execute(insert_sql, sql_data)
        conn.commit()

    except sqlite3.Error as e:
        print(f"[ERROR] Database operation failed: {e}")
    finally:
        conn.close()
    
    try:
        env = Environment(loader=FileSystemLoader(BASE_DIR))
        template = env.get_template(os.path.basename(TEMPLATE_PATH))

        content = template.render({
            "app_name": app_name,
            "app_port": app_port,
            "ip_addr": ip_address
        })

        config_file_path = os.path.join(NGNIX_FILE_PATH, f"{id_}.conf")
        with open(config_file_path, 'w') as file:
            file.write(content)

    except Exception as e:
        print(f"[ERROR] Failed to generate Nginx config: {e}")


if __name__ == "__main__":
    deploy_app()

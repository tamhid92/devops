import sqlite3
import datetime
import json
import os
from jinja2 import Environment, FileSystemLoader

BASE_DIR = "/home/tamhid/ansible"
DB_PATH = os.path.join(BASE_DIR, "database.sqlite")
JSON_PATH = os.path.join(BASE_DIR, "app_vars.json")
TEMPLATE_PATH = os.path.join(BASE_DIR, "nginix-conf.conf.j2")

def deploy_app():

    try:
        with open(JSON_PATH, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERROR] Failed to read JSON file: {e}")
        return

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
            f'''["{data['app_name']}.tchowdhury.org"]''',
            data['ip_addr'], data['app_port'], '0', '11', '1', '0', '1', '',
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

        try:
            env = Environment(loader=FileSystemLoader(BASE_DIR))
            template = env.get_template(os.path.basename(TEMPLATE_PATH))

            content = template.render(data)

            config_file_path = os.path.join(BASE_DIR, f"{id_}.conf")
            with open(config_file_path, 'w') as file:
                file.write(content)
            
            return id_

        except Exception as e:
            print(f"[ERROR] Failed to generate Nginx config: {e}")
    except sqlite3.Error as e:
        print(f"[ERROR] Database operation failed: {e}")
    finally:
        conn.close()



if __name__ == "__main__":

    id_ = deploy_app()
    print(id_)

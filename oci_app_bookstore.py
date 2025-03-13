from flask import Flask, render_template
import mysql.connector
import oci
import base64
import socket

app = Flask(__name__)

def get_config(region):
    return oci.config.from_file(profile_name=region)

config_location = get_config("sa-bogota-1")                                       ################### PLACE HOLDER ####################


# Initialize the SecretsClient
secrets_client = oci.secrets.SecretsClient(config_location)

# Retrieve the vault secrets IDs from the local file: /home/opc/vault_secret_ocids.txt

file_path = '/home/opc/vault_secret_ocids.txt'
vault_secrets_ocid_list = []
with open(file_path, 'r') as file:
    vault_secrets_ocid_list = file.read().splitlines()


vault_user = vault_secrets_ocid_list[0]
vault_password = vault_secrets_ocid_list[1]
vault_database = vault_secrets_ocid_list[2]
vault_host = vault_secrets_ocid_list[3]


# Retrieve the vault secrets contents

response = secrets_client.get_secret_bundle(vault_user)
vault_user_value = response.data.secret_bundle_content.content
oci_dbsystem_user = base64.b64decode(vault_user_value).decode('utf-8')

response = secrets_client.get_secret_bundle(vault_password)
vault_password_value = response.data.secret_bundle_content.content
oci_dbsystem_password = base64.b64decode(vault_password_value).decode('utf-8')

response = secrets_client.get_secret_bundle(vault_database)
vault_database_value = response.data.secret_bundle_content.content
oci_dbsystem_database = base64.b64decode(vault_database_value).decode('utf-8')

response = secrets_client.get_secret_bundle(vault_host)
vault_host_value = response.data.secret_bundle_content.content
oci_dbsystem_host = base64.b64decode(vault_host_value).decode('utf-8')


@app.route('/')
def home():
    opc_hostname = socket.gethostname()
    ip_address = socket.gethostbyname(opc_hostname)
    return render_template("index.html",ip_address=ip_address)

@app.route('/libros')
def libros():
    opc_hostname = socket.gethostname()
    ip_address = socket.gethostbyname(opc_hostname)    
    conn = mysql.connector.connect(
        host=oci_dbsystem_host,
        user=oci_dbsystem_user,
        password=oci_dbsystem_password,
        database=oci_dbsystem_database)
    
    c = conn.cursor()
    c.execute("SELECT * FROM Books")
    books = c.fetchall()
    conn.close()
    return render_template("libros.html", books=books, ip_address=ip_address)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
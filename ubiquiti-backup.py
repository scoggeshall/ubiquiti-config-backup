import os
import csv
import json
import ipaddress
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import paramiko
from scp import SCPClient

# === Paths & Setup ===
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, "data")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

LOG_FILE = os.path.join(BACKUP_DIR, "backup.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# === Load Credentials ===
with open(os.path.join(DATA_DIR, "credentials.json")) as f:
    creds = json.load(f)
USERNAME = creds["username"]
PASSWORD = creds["password"]

# === Load & Validate IPs ===
valid_ips = []
with open(os.path.join(DATA_DIR, "ip_list.csv"), newline="") as csvf:
    for row in csv.DictReader(csvf):
        ip_raw = row.get("ip", "").strip()
        try:
            valid_ips.append(str(ipaddress.ip_address(ip_raw)))
        except ValueError:
            logging.warning(f"Skipped invalid IP: {ip_raw}")

REMOTE_PATH = "/var/tmp/system.cfg"
TODAY       = datetime.utcnow().date().isoformat()

def backup_device(ip):
    """Connect via SSH, SCP the config, and log results."""
    dest_dir  = os.path.join(BACKUP_DIR, ip, TODAY)
    os.makedirs(dest_dir, exist_ok=True)
    dest_file = os.path.join(dest_dir, os.path.basename(REMOTE_PATH))

    if os.path.exists(dest_file):
        logging.info(f"{ip} – already backed up today")
        return

    try:
        # Establish SSH session
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=USERNAME, password=PASSWORD, timeout=10)

        # SCP transfer
        scp = SCPClient(ssh.get_transport())
        scp.get(REMOTE_PATH, dest_file)
        scp.close()
        ssh.close()

        logging.info(f"{ip} – SUCCESS")
    except Exception as e:
        logging.error(f"{ip} – FAILURE: {e}")

if __name__ == "__main__":
    print("[*] Starting backup run")
    # Use up to 8 threads—tune as needed
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(backup_device, ip): ip for ip in valid_ips}
        for future in as_completed(futures):
            ip = futures[future]
            # Exceptions already logged inside backup_device
    print("[*] Backup run complete")

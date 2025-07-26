# Ubiquiti Config Backup

A simple Python script to back up Ubiquiti device configs (`/var/tmp/system.cfg`) over SCP.

## Features

- Saves to `backups/<ip>/<YYYY-MM-DD>/system.cfg`
- Parallel execution using `ThreadPoolExecutor`
- Skips devices already backed up today (idempotent)
- Logs activity to `backups/backup.log`

## Setup

```bash
git clone https://github.com/scoggeshall/ubiquiti-config-backup.git
cd ubiquiti-config-backup
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
pip install -r requirements.txt
```

## Configure

### Credentials (`data/credentials.json`)

```json
{
  "username": "ubnt",
  "password": "ubnt"
}
```

### IP List (`data/ip_list.csv`)

```csv
ip
192.168.1.10
192.168.1.11
```

## Run

```bash
python ubiquiti-backup.py
```

## Output

- Configs saved to: `backups/<ip>/<YYYY-MM-DD>/system.cfg`
- Log file: `backups/backup.log`

## License

MIT

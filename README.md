# Ubiquiti Config Backup Tool

Automates pulling `/var/tmp/system.cfg` from Ubiquiti devices (e.g., NanoStation M5) over SCP and stores dated backups locally.

## Features

- SCP download of `/var/tmp/system.cfg` from each device
- Per-device, per-day directory structure: `backups/<ip>/<YYYY-MM-DD>/system.cfg`
- Structured logging to `backups/backup.log`
- Skips devices already backed up today (idempotent)
- Parallel transfers using `ThreadPoolExecutor`
- Credentials and IP list loaded from flat files

## Repository Layout

ubiquiti-config-backup/
├── backups/                 # Generated backups + logs (gitignored)
│   └── backup.log
├── data/                    # Local data (not committed)
│   ├── credentials.json
│   └── ip_list.csv
├── requirements.txt         # Python dependencies
├── ubiquiti-backup.py       # Main script
└── .gitignore

## Prerequisites

- Python 3.8+
- Git
- Network access to Ubiquiti devices over SSH/SCP

## Install

```bash
git clone https://github.com/scoggeshall/ubiquiti-config-backup.git
cd ubiquiti-config-backup
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
pip install -r requirements.txt

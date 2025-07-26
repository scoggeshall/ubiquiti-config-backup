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

```text
ubiquiti-config-backup/
├── backups/                 # Generated backups + logs (gitignored)
│   └── backup.log
├── data/                    # Local data
│   ├── credentials.json
│   └── ip_list.csv
├── requirements.txt         # Python dependencies
├── ubiquiti-backup.py       # Main script
└── .gitignore
```

## Prerequisites

* Python 3.8+
* Git
* Network access to Ubiquiti devices over SSH/SCP

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
```

## Configure

### Credentials (`data/credentials.json`):

```json
{
  "username": "ubnt",
  "password": "ubnt"
}
```

### Device list (`data/ip_list.csv`):

```csv
ip
192.168.1.10
192.168.1.11
```

## Run

```bash
python ubiquiti-backup.py
```

Backups → `backups/<ip>/<YYYY-MM-DD>/system.cfg`  
Logs → `backups/backup.log`

## .gitignore

```gitignore
backups/
__pycache__/
*.pyc
*.log
```

## Scheduling

### Windows Task Scheduler

* Program/script: `venv\Scripts\python.exe`
* Add arguments: `ubiquiti-backup.py`
* Start in: repo root
* Trigger: daily at 2:00 AM

### Cron (Linux/macOS)

```cron
0 2 * * * /path/to/venv/bin/python /path/to/ubiquiti-backup.py
```

## Troubleshooting

* **Auth errors**: verify credentials
* **SCP hangs**: check firmware compatibility
* **Missing file**: confirm `/var/tmp/system.cfg` exists
* **Timeouts**: ensure port 22 is reachable

## Roadmap

* Config diffing + alerts
* HTML/Markdown reports
* Slack/email notifications
* CMDB/NetBox integration

## License

MIT

## Contributing

Fork → branch → PR. Keep secrets out of commits.

---

### Next Steps

1. **Allow `credentials.json` into Git**

   * Edit `.gitignore` and remove the line `data/credentials.json`.

2. **Stage changes**

```powershell
git add README.md .gitignore data/credentials.json
```

3. **Commit**

```powershell
git commit -m "docs: fix README formatting; track credentials.json"
```

4. **Push**

```powershell
git push origin main
```

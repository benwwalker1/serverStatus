# serverStatus

Lab server monitoring dashboard deployed via GitHub Pages.

## After pushing code changes

After every push, give the user these update instructions:

### Update on the leader server (nsc1)

SSH into nsc1 and pull the latest code:

```bash
cd ~/server_monitor
git pull origin main
```

The changes take effect on the next cron cycle (runs every 5 minutes). The dashboard at GitHub Pages will update automatically once the next monitoring cycle completes and pushes `dashboard.json`.

### If process_data.py or monitor.sh changed

No restart needed -- cron re-executes `monitor.sh` every 5 minutes, which calls `process_data.py` fresh each run.

### If index.html changed

The frontend is served directly from the `main` branch via GitHub Pages. It updates as soon as GitHub Pages rebuilds (typically within a minute of the push).

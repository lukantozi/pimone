# Pimone - Linux System Monitor

An OOP-based system monitor written in Python that reads Linux system information directly from `/proc` and displays it in a real-time web dashboard.

## How it works

- A background **agent** collects metrics every few seconds and POSTs them to a Flask server
- The **server** keeps a rolling 20-minute window of data and exposes it via a REST API
- A **browser dashboard** polls `/status` every 3 seconds and updates charts and gauges in real time

## Project structure

```
pimone/
├── agent/
│   └── agent.py              # Collects all metrics and POSTs to the server
├── collectors/
│   ├── base.py               # Abstract MetricCollector base class
│   ├── cpu.py                # Reads /proc/stat, computes CPU usage %
│   ├── memory.py             # Reads /proc/meminfo, computes used/total RAM
│   └── disk.py               # Reads /proc/mounts + statvfs, per-mount usage
├── process.py                # Reads /proc/<pid>/stat, per-process CPU and memory
├── server/
│   ├── app.py                # Flask API: /metrics (POST), /status (GET), / (dashboard)
│   ├── store.py              # RollingStore: time-keyed dict with average/peak helpers
│   ├── static/
│   │   └── pimone.js         # All frontend logic: charts, gauges, history, window buttons
│   └── templates/
│       └── pimone_raw.html   # Dashboard HTML layout
```

## Collectors

All collectors inherit from `MetricCollector` (abstract base class) and implement:
- `collect()` -- reads raw data from the filesystem
- `format_data()` -- parses and returns a clean dict

| Collector | Source | Output |
|---|---|---|
| `CPUCollector` | `/proc/stat` | Overall + per-core CPU % (1-second sample delta) |
| `MemoryCollector` | `/proc/meminfo` | MemTotal, MemFree, MemUsed, Cached (GB) |
| `DiskCollector` | `/proc/mounts` + `statvfs` | Per-mount total/used/free in K/M/G |
| `ProcessMonitor` | `/proc/<pid>/stat` | Per-process lifetime CPU % and memory, sorted by CPU |

## Server

- `POST /metrics` -- receives a JSON snapshot from the agent and stores it in `RollingStore`
- `GET /status` -- returns all stored snapshots as `{ timestamp: data_dict }`
- `GET /` -- serves the dashboard HTML

`RollingStore` keeps the last 20 minutes of snapshots and exposes `.average` and `.peak` as properties.

## Dashboard

The browser dashboard (`pimone.js`) polls `/status` every 3 seconds and:
- Keeps up to 1 hour of history in memory
- Shows a live CPU % + Memory GB dual-axis line chart
- Supports 5m / 10m / 20m / 60m visible window buttons with peak markers (red dots)
- Shows 4 half-circle gauges: CPU, Memory, Disk /, Top process
- Shows a live process table (top 10 by CPU) and a disk mount table
- Reads `cores` and `MemTotal` from the backend to normalize values dynamically (no hardcoded machine specs)

## Running

Start the Flask server:
```bash
cd server
python app.py
```

Start the agent (separate terminal):
```bash
cd agent
python agent.py
```

Then open `http://localhost:5000` in a browser.

## Goal

OOP course project focused on practicing inheritance, abstract 
classes, properties, encapsulation, and building a full small 
application from scratch -- from raw `/proc` reads to a live 
browser dashboard.

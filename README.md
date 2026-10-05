# pimone

Linux system monitor in Python with a web dashboard.

## Setup

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```sh
python server/app.py
```

In another terminal:

```sh
python agent/agent.py
```

Open http://localhost:5000 in a browser.

## License

MIT

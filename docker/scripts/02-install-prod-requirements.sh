# /bin/bash

virtualenv -p /usr/bin/python3.9 venv
venv/bin/pip install pip-tools
venv/bin/pip-compile -U requirements.in -o requirements.txt
venv/bin/pip install -r requirements.txt
venv/bin/pip install gunicorn
venv/bin/pip install uvicorn

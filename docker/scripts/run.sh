# /bin/bash

/app/venv/bin/gunicorn root.asgi:application -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:8000

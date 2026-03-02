#!/bin/sh
set -e
# Start backend in background
uvicorn main:app --host 127.0.0.1 --port 8000 &
# Start nginx (foreground)
exec nginx -g "daemon off;"

#!/bin/sh
source venv/bin/activate
exec gunicorn -b :5000 -w 4 --timeout 90 --access-logfile - --error-logfile - app:app
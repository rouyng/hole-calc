"""Gunicorn configuration for the hole calc Docker image."""
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"
workers = int(os.environ.get('WEB_CONCURRENCY', '4'))
# Requests take milliseconds; a worker silent this long is stuck and gets replaced.
# Keep below the reverse proxy's read timeout (nginx default: 60s).
timeout = 30
graceful_timeout = 30  # time workers get to finish in-flight requests on restart
worker_tmp_dir = "/dev/shm"  # avoid heartbeat stalls on overlay filesystems in Docker
accesslog = "-"
errorlog = "-"

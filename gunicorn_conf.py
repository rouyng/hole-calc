"""Gunicorn configuration for the hole calc Docker image."""
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8080')}"
workers = int(os.environ.get('WEB_CONCURRENCY', '4'))
timeout = 1000  # carried over from the previous image, where workers were timing out
worker_tmp_dir = "/dev/shm"  # avoid heartbeat stalls on overlay filesystems in Docker
accesslog = "-"
errorlog = "-"

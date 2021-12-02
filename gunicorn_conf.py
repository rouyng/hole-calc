# Configuration file for Gunicorn. Included because the base docker image was timing out workers
workers = 4  # Define the number of processes to be opened for processing requests at the same time
timeout = 2000

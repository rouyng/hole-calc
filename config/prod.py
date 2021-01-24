"""Flask configuration for production environment"""
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set in environment variables!")
TESTING = False
WTF_CSRF_ENABLED = True
HASH_ROUNDS = 1

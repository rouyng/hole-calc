"""Flask configuration for test environment"""
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-placeholder-key'
TESTING = True
WTF_CSRF_ENABLED = False
HASH_ROUNDS = 1
DEBUG = False

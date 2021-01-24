"""Flask configuration for development environment"""
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
TESTING = False
SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-placeholder-key'
WTF_CSRF_ENABLED = False
DEBUG = True

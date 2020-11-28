import os


class Config(object):
    """Base config, all others inherit from this"""
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    """Config for development environment"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'some-placeholder-key'
    DEBUG = True


class TestConfig(Config):
    """Config for testing"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    HASH_ROUNDS = 1

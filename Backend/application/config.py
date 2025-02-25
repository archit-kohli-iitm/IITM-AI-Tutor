import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    DEBUG = False
    TESTING = False
    CACHE_TYPE = "null"
    
class DevConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///seproject.db'
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    SECURITY_PASSWORD_HASH = "bcrypt"
    WTF_CSRF_ENABLED = False
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 3
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
    JWT_SECRET_KEY = 'f3a1b8d57e46b6fbe29c84e5a7d3c8d092c13e2fa8f72f9bb9b3a50f2938a1b4'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

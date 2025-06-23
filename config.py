import os
from dotenv import load_dotenv

load_dotenv()

# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_MYSQL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #https://flask-sqlalchemy.readthedocs.io/en/stable/config/
    SQLALCHEMY_ENGINE_OPTIONS = { 'pool_recycle': 280, 'pool_pre_ping': True }
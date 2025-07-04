import os
from dotenv import load_dotenv

# config.py
class Config:
    #
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or os.environ.get('CSRF_SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_MYSQL')
    if SQLALCHEMY_DATABASE_URI :
      #print("found DB setting")
      pass
    else :
      #did not found env setting, read from .env file
      load_dotenv()
      SQLALCHEMY_DATABASE_URI = os.getenv('DB_MYSQL')
      SECRET_KEY = os.getenv('FLASK_SECRET_KEY') or os.getenv('CSRF_SECRET')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #https://flask-sqlalchemy.readthedocs.io/en/stable/config/
    SQLALCHEMY_ENGINE_OPTIONS = { 'pool_recycle': 280, 'pool_pre_ping': True }

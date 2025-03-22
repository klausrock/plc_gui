import os
from dotenv import load_dotenv

# Load environment variables from the .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '../.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, '../data.sqlite'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
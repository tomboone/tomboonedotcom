""" Configurations for Flask Application """
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
SITE_NAME = os.getenv('FLASK_SITE_NAME')

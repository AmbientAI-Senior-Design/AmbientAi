import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
PORT = os.getenv('PORT')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_USER = os.getenv('MYSQL_USER')

application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = os.path.join('src', 'static', 'uploads')

STATIC_FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
PORT = os.getenv('PORT')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_USER = os.getenv('MYSQL_USER')
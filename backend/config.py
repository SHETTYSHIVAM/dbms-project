from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
import urllib

load_dotenv()

# ACCESS THE VARIABLES
MYSQL_USER = os.getenv('MYSQL_USERNAME')
MYSQL_PASSWORD = MYSQL_PASSWORD = urllib.parse.quote_plus(os.getenv('MYSQL_PASSWORD'))  # Encode special characters
MYSQL_DB = os.getenv('MYSQL_DB')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')

app = Flask(__name__)
CORS(app)

# Use mysql-connector-python with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

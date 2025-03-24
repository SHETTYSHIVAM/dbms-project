from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os
import urllib
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
load_dotenv()



# ACCESS THE VARIABLES
MYSQL_USER = os.getenv('MYSQL_USERNAME')
MYSQL_PASSWORD = MYSQL_PASSWORD = urllib.parse.quote_plus(os.getenv('MYSQL_PASSWORD'))  # Encode special characters
MYSQL_DB = os.getenv('MYSQL_DB')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/book_images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# Use mysql-connector-python with SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bycrypt = Bcrypt()
jwt = JWTManager()

# Initialize Flask-Migrate
migrate = Migrate(app, db)
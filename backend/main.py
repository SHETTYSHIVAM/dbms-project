from flask import request, jsonify
from config import app, db
from models import *

# Create the tables (if they don't exist already)
with app.app_context():
    db.create_all()

@app.route("/", methods=['GET'])
def index():
    return "Hello"

if __name__=="__main__":
    app.run(debug=True)
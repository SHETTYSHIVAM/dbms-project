from flask import request, jsonify
from config import app, db
from models import *
from routes.books import books
from routes.users import users
from routes.auth import auth

# Create the tables (if they don't exist already)
with app.app_context():
    db.create_all()

app.register_blueprint(books)
app.register_blueprint(users)
app.register_blueprint(auth)

@app.route("/", methods=['GET'])
def index():
    return "Hello"



if __name__=="__main__":
    app.run(debug=True)
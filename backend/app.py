from flask import request, jsonify
from config import app, db
from models import *
from routes.books import books
from routes.users import users
from routes.auth import auth
from models import TokenBlocklist
from config import jwt

# Create the tables (if they don't exist already)
with app.app_context():
    db.create_all()

app.register_blueprint(books)
app.register_blueprint(users)
app.register_blueprint(auth)

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar() is not None
@app.route("/", methods=['GET'])
def index():
    return "Hello"

if __name__=="__main__":
    app.run(debug=True)
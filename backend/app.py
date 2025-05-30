from backend.config import app
from backend.config import jwt
from backend.models import *
from backend.routes.auth import auth
from backend.routes.books import books
from backend.routes.dashboard import dashboard
from backend.routes.reservations import reservations
from backend.routes.transactions import transactions
from backend.routes.users import users

# Create the tables (if they don't exist already)
with app.app_context():
    db.create_all()

app.register_blueprint(books)
app.register_blueprint(users)
app.register_blueprint(auth)
app.register_blueprint(transactions)
app.register_blueprint(reservations)
app.register_blueprint(dashboard)


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar() is not None


@app.route("/", methods=['GET'])
def index():
    return "Hello"


if __name__ == "__main__":
    app.run(debug=True)

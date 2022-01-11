import os
import sys

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
# from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout

# TODO: models - user, pet, claw, session
# TODO: resources - user (UserRegister, UserLogin, User, TokenRefresh, UserLogout, ForgotPassword, UpdatePassword),
# TODO: resources - pet (Pet, PetList),
# TODO: resources - claw (Claw), <= do I need to do that? I will probably just need a session endpoints
# TODO: resources - session (Session, SessionList)

sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "jose"  # could do app.config['JWT_SECRET_KEY'] if we prefer
api = Api(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@app.route('/')
def api():
    return {
        "status": "success",
        "message": "Test API",
    }

# api.add_resource(UserRegister, "/register")
# api.add_resource(User, "/user/<int:user_id>")
# api.add_resource(UserLogin, "/login")
# api.add_resource(TokenRefresh, "/refresh")
# api.add_resource(UserLogout, "/logout")

application = app

import os
import sys

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from db import db
# from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.user import User
from resources.group import Group, GroupCreate, GroupList
from models.pet import PetModel
from models.claw import ClawModel
from models.session import SessionModel
from models.session_data import SessionDataModel


# TODO: resources - user (UserRegister, UserLogin, User, TokenRefresh, UserLogout, ForgotPassword, UpdatePassword),
# TODO: resources - pet (Pet, PetList),
# TODO: resources - claw (Claw), <= do I need to do that? I will probably just need a session endpoints
# TODO: resources - session (Session, SessionList)

sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_pyfile("./config.py")
app.secret_key = "jose"  # could do app.config['JWT_SECRET_KEY'] if we prefer
api = Api(app)
bcrypt = Bcrypt(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@app.route('/')
def api_homepage():
    return {
        "status": "success",
        "message": "Test API",
    }


api.add_resource(Group, "/group/<int:id>")
api.add_resource(GroupCreate, "/group")
api.add_resource(GroupList, "/groups")
# api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
# api.add_resource(UserLogin, "/login")
# api.add_resource(TokenRefresh, "/refresh")
# api.add_resource(UserLogout, "/logout")

application = app

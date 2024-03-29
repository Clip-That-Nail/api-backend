import os
import sys

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError

from db import db
from ma import ma
from blocklist import BLOCKLIST
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.group import Group, GroupCreate, GroupList
from resources.pet import Pet, PetCreate, PetList
from resources.claw import ClawList
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

db.init_app(app)
ma.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)


# This method will check if a token is blocklisted, and will be called automatically when blocklist is enabled
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@app.route('/')
def api_homepage():
    return {
        "status": "success",
        "message": "Test API",
    }


api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(Group, "/group/<int:id>")
api.add_resource(GroupCreate, "/group")
api.add_resource(GroupList, "/groups")
api.add_resource(Pet, "/pet/<int:id>")
api.add_resource(PetCreate, "/pet")
api.add_resource(PetList, "/pets")
api.add_resource(ClawList, "/claws/<int:pet_id>")

application = app

from flask import request
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from datetime import datetime
from models.user import UserModel
from schemas.user import UserSchema
from blocklist import BLOCKLIST

USER_ALREADY_EXISTS = "A user with that email already exists."
CREATED_SUCCESSFULLY = "User created successfully."
ERROR_REGISTERING = "An error occurred while registering a new user."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={}> successfully logged out."

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()

        if UserModel.find_by_email(user_json["email"]):
            return {"message": USER_ALREADY_EXISTS}, 400

        user_json["password"] = generate_password_hash(user_json["password"])
        user_json["must_change_password"] = False
        user_json["status"] = 0
        user_json["created_at"] = str(datetime.utcnow())
        user_json["updated_at"] = str(datetime.utcnow())
        user = user_schema.load(user_json)

        try:
            user.save_to_db()
        except Exception as err:
            print(str(err)) # TODO: use some kind of logger?
            return {"message": ERROR_REGISTERING}, 500

        return {"message": CREATED_SUCCESSFULLY}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        return user_schema.dump(user), 200

    @classmethod
    @jwt_required(refresh=True)
    def delete(cls, user_id: int):
        # TODO: check if user using it is an Admin
        # user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()

        user = UserModel.find_by_email(user_json["email"])

        if user and check_password_hash(user.password, user_json["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        # jti is "JWT ID", a unique identifier for a JWT.
        jti = get_jwt()["jti"]
        user_id = get_jwt_identity()
        BLOCKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        # TODO: should I check blocked jti ? should user be able to refresh token that is already logged out
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200

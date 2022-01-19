from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from datetime import datetime
from models.user import UserModel
from blocklist import BLOCKLIST

BLANK_ERROR = "'{}' cannot be blank."
USER_ALREADY_EXISTS = "A user with that email already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={user_id}> successfully logged out."


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "group_id", type=int, required=True, help=BLANK_ERROR.format("group_id")
    )
    parser.add_argument(
        "first_name", type=str, required=True, help=BLANK_ERROR.format("first_name")
    )
    parser.add_argument(
        "last_name", type=str, required=True, help=BLANK_ERROR.format("last_name")
    )
    parser.add_argument(
        "email", type=str, required=True, help=BLANK_ERROR.format("email")
    )
    parser.add_argument(
        "password", type=str, required=True, help=BLANK_ERROR.format("password")
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        if UserModel.find_by_email(data["email"]):
            return {"message": USER_ALREADY_EXISTS}, 400

        user = UserModel(
            data["group_id"],
            data["first_name"],
            data["last_name"],
            data["email"],
            data["password"],
            False,
            0,
            datetime.now(),
            datetime.now()
        )
        user.save_to_db()

        return {"message": CREATED_SUCCESSFULLY}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        return user.json(), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404
        user.delete_from_db()
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str, required=True, help=BLANK_ERROR.format("email")
    )
    parser.add_argument(
        "password", type=str, required=True, help=BLANK_ERROR.format("password")
    )

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()

        user = UserModel.find_by_email(data["email"])

        if user and check_password_hash(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLOCKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200

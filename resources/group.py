from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from datetime import datetime
from models.group import GroupModel

BLANK_ERROR = "'{}' cannot be blank."
NAME_ALREADY_EXISTS = "A group with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting a new group."
GROUP_NOT_FOUND = "Group not found."
GROUP_DELETED = "Group deleted."


class Group(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=float, required=True, help=BLANK_ERROR.format("name")
    )

    @classmethod
    def get(cls, id: int):
        group = GroupModel.find_by_id(id)
        if group:
            return group.json(), 200
        return {"message": GROUP_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def post(cls):
        data = cls.parser.parse_args()

        if GroupModel.find_by_name(data["name"]):
            return {"message": NAME_ALREADY_EXISTS.format(data["name"])}, 400

        group = GroupModel(data["name"], datetime.now(), datetime.now())

        try:
            group.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return group.json(), 201

    @classmethod
    @jwt_required()
    def delete(cls, id: int):
        group = GroupModel.find_by_id(id)
        if group:
            group.delete_from_db()
            return {"message": GROUP_DELETED}, 200
        return {"message": GROUP_NOT_FOUND}, 404

    @classmethod
    def put(cls, id: int):
        data = cls.parser.parse_args()

        group = GroupModel.find_by_id(id)

        if group:
            group.name = data["name"]
            group.updated_at = datetime.now()
        else:
            group = GroupModel(data["name"], datetime.now(), datetime.now())

        group.save_to_db()

        return group.json(), 200


class GroupList(Resource):
    @classmethod
    def get(cls):
        return {"groups": [group.json() for group in GroupModel.find_all()]}, 200

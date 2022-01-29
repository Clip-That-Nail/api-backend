from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from datetime import datetime
from models.group import GroupModel
from schemas.group import GroupSchema

NAME_ALREADY_EXISTS = "A group with name '{}' already exists."
ERROR_INSERTING = "An error occurred while {} a new group."
GROUP_NOT_FOUND = "Group not found."
GROUP_DELETED = "Group deleted."

group_schema = GroupSchema()
group_list_schema = GroupSchema(many=True)


class Group(Resource):

    @classmethod
    def get(cls, id: int):
        group = GroupModel.find_by_id(id)
        if group:
            return group_schema.dump(group), 200
        return {"message": GROUP_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, id: int):
        group = GroupModel.find_by_id(id)
        if group:
            group.delete_from_db()
            return {"message": GROUP_DELETED}, 200
        return {"message": GROUP_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def put(cls, id: int):
        group_json = request.get_json()
        group = GroupModel.find_by_id(id)
        process = ""

        if group:
            group.name = group_json["name"]
            group.updated_at = str(datetime.utcnow())
            process = "updating"
        else:
            group_json["created_at"] = str(datetime.utcnow())
            group_json["updated_at"] = str(datetime.utcnow())
            group = group_schema.load(group_json)
            process = "inserting"

        try:
            group.save_to_db()
        except:
            return {"message": ERROR_INSERTING.format(process)}, 500

        return group_schema.dump(group), 200


class GroupCreate(Resource):

    @classmethod
    @jwt_required(fresh=True)
    def post(cls):
        group_json = request.get_json()

        if GroupModel.find_by_name(group_json["name"]):
            return {"message": NAME_ALREADY_EXISTS.format(group_json["name"])}, 400

        group_json["created_at"] = str(datetime.utcnow())
        group_json["updated_at"] = str(datetime.utcnow())
        group = group_schema.load(group_json)

        try:
            group.save_to_db()
        except:
            return {"message": ERROR_INSERTING.format("inserting")}, 500

        return group_schema.dump(group), 201


class GroupList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        return {"groups": group_list_schema.dump(GroupModel.find_all())}, 200

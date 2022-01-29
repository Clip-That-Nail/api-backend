from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from datetime import datetime
from models.session import SessionModel
from models.session_data import SessionDataModel
from schemas.session import SessionSchema
from schemas.session_data import SessionDataSchema

BLANK_ERROR = "{} cannot be blank."
NAME_ALREADY_EXISTS = "A session with name '{}' already exists."
ERROR_INSERTING = "An error occurred while {} a new session."
SESSION_NOT_FOUND = "Session not found."
SESSION_DELETED = "Session deleted."

session_schema = SessionSchema()
session_list_schema = SessionSchema(many=True)
session_data_schema = SessionDataSchema()


class Session(Resource):

    @classmethod
    @jwt_required()
    def get(cls, id: int):
        user_id = get_jwt_identity()

        session = SessionModel.find_one_by_user_id(id, user_id)
        if session:
            return session_schema.dump(session), 200
        return {"message": SESSION_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, id: int):
        user_id = get_jwt_identity()

        session = SessionModel.find_one_by_user_id(id, user_id)

        all_session_data = SessionDataModel.find_all_by_session_id(id)
        for session_data in all_session_data:
            session_data.delete_from_db()

        if session:
            session.delete_from_db()
            return {"message": SESSION_DELETED}, 200
        return {"message": SESSION_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def put(cls, id: int):
        session_json = request.get_json()
        user_id = get_jwt_identity()

        session = SessionModel.find_one_by_user_id(id, user_id)
        process = ""

        if session:
            session.status = session_json["status"]
            session.pet_id = session_json["pet_id"]
            session.updated_at = str(datetime.utcnow())

            for session_data in session_json["data"]:
                existing_session_data = SessionDataModel.find_one_by_session_id_and_claw(
                    id, session_data["paw"], session_data["claw"])
                if existing_session_data:
                    existing_session_data.paw = session_data["paw"]
                    existing_session_data.claw = session_data["claw"]
                    existing_session_data.status = session_data["status"]
                    existing_session_data.outcome = session_data["outcome"]
                    existing_session_data.behaviour = session_data["behaviour"]
                    existing_session_data.updated_at = str(datetime.utcnow())
                else:
                    session_data["session_id"] = id
                    session_data["created_at"] = str(datetime.utcnow())
                    session_data["updated_at"] = str(datetime.utcnow())
                    existing_session_data = session_data_schema.load(
                        session_data)

                existing_session_data.save_to_db()

            process = "updating"
        else:
            session_json["user_id"] = user_id
            session_json["created_at"] = str(datetime.utcnow())
            session_json["updated_at"] = str(datetime.utcnow())

            for session_data in session_json["data"]:
                session_data["session_id"] = id
                session_data["created_at"] = str(datetime.utcnow())
                session_data["updated_at"] = str(datetime.utcnow())

            session = session_schema.load(session_data)
            process = "inserting"

        try:
            session.save_to_db()
        except:
            return {"message": ERROR_INSERTING.format(process)}, 500

        return session_schema.dump(session), 200


class SessionCreate(Resource):

    @classmethod
    @jwt_required()
    def post(cls):
        session_json = request.get_json()
        user_id = get_jwt_identity()

        session_json["user_id"] = user_id
        session_json["created_at"] = str(datetime.utcnow())
        session_json["updated_at"] = str(datetime.utcnow())

        for session_data in session_json["data"]:
            session_data["session_id"] = id
            session_data["created_at"] = str(datetime.utcnow())
            session_data["updated_at"] = str(datetime.utcnow())

        session = session_schema.load(session_data)

        try:
            session.save_to_db()
        except:
            return {"message": ERROR_INSERTING.format("inserting")}, 500

        return session_schema.dump(session), 201


class SessionList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        user_id = get_jwt_identity()
        return {"sessions": session_list_schema.dump(SessionModel.find_all_by_user_id(user_id))}, 200

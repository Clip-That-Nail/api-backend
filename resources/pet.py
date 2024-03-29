from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from datetime import datetime
from models.pet import PetModel
from models.claw import ClawModel
from schemas.pet import PetSchema
from schemas.claw import ClawSchema

BLANK_ERROR = "{} cannot be blank."
NAME_ALREADY_EXISTS = "A pet with name '{}' already exists."
ERROR_INSERTING = "An error occurred while {} a new pet."
PET_NOT_FOUND = "Pet not found."
PET_DELETED = "Pet deleted."

pet_schema = PetSchema()
pet_list_schema = PetSchema(many=True)
claw_schema = ClawSchema()


class Pet(Resource):

    @classmethod
    @jwt_required()
    def get(cls, id: int):
        user_id = get_jwt_identity()

        pet = PetModel.find_one_by_user_id(id, user_id)
        if pet:
            return pet_schema.dump(pet), 200
        return {"message": PET_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, id: int):
        user_id = get_jwt_identity()

        pet = PetModel.find_one_by_user_id(id, user_id)

        claws = ClawModel.find_all_by_pet_id(id)
        for claw in claws:
            claw.delete_from_db()

        if pet:
            pet.delete_from_db()
            return {"message": PET_DELETED}, 200
        return {"message": PET_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def put(cls, id: int):
        pet_json = request.get_json()
        user_id = get_jwt_identity()

        pet = PetModel.find_one_by_user_id(id, user_id)
        process = ""

        if pet:
            pet.name = pet_json["name"]
            pet.type = pet_json["type"]
            pet.breed = pet_json["breed"]
            pet.image_uri = pet_json["image_uri"]
            pet.disabled = bool(pet_json["disabled"])
            pet.updated_at = str(datetime.utcnow())

            for claw_data in pet_json["claws"]:
                claw = ClawModel.find_one_by_pet_id_and_name(
                    id, claw_data["name"], claw_data["paw"])
                if claw:
                    claw.name = claw_data["name"]
                    claw.paw = claw_data["paw"]
                    claw.disabled = bool(claw_data["disabled"])
                    claw.skipped = bool(claw_data["skipped"])
                    claw.skip_length = int(claw_data["skip_length"])
                    claw.updated_at = str(datetime.utcnow())
                else:
                    # claw_data["pet_id"] = id   # TODO: problem with foreign keys included when creating or updating pet with claws data... when creating I don't have pet_id, but I have it and I need to have it (probably) when updating.  I think I need to remove include_fk in schemas and just use db.ForeignKey (that will probably do the trick?) or other way - use include_fk instead db.ForeignKey ???
                    claw_data["created_at"] = str(datetime.utcnow())
                    claw_data["updated_at"] = str(datetime.utcnow())
                    claw = claw_schema.load(claw_data)

                claw.save_to_db()

            process = "updating"
        else:
            pet_json["user_id"] = user_id
            pet_json["created_at"] = str(datetime.utcnow())
            pet_json["updated_at"] = str(datetime.utcnow())

            for claw in pet_json["claws"]:
                claw["created_at"] = str(datetime.utcnow())
                claw["updated_at"] = str(datetime.utcnow())

            pet = pet_schema.load(pet_json)
            process = "inserting"

        try:
            pet.save_to_db()
        except:
            return {"message": ERROR_INSERTING.format(process)}, 500

        return pet_schema.dump(pet), 200


class PetCreate(Resource):

    @classmethod
    @jwt_required()
    def post(cls):
        pet_json = request.get_json()
        user_id = get_jwt_identity()

        # Should we check if Pet exist?
        # if PetModel.find_by_name(data["name"]):
        #     return {"message": NAME_ALREADY_EXISTS.format(data["name"])}, 400

        pet_json["user_id"] = user_id
        pet_json["created_at"] = str(datetime.utcnow())
        pet_json["updated_at"] = str(datetime.utcnow())

        for claw in pet_json["claws"]:
            claw["created_at"] = str(datetime.utcnow())
            claw["updated_at"] = str(datetime.utcnow())

        pet = pet_schema.load(pet_json)

        try:
            pet.save_to_db()
        except:
            return {"message": ERROR_INSERTING.format("inserting")}, 500

        return pet_schema.dump(pet), 201


class PetList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        user_id = get_jwt_identity()
        return {"pets": pet_list_schema.dump(PetModel.find_all_by_user_id(user_id))}, 200

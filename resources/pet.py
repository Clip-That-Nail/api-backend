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

# _pet_parser = reqparse.RequestParser()
# _pet_parser.add_argument(
#     "name", type=str, required=True, help=BLANK_ERROR.format("Pet name"), location='json'
# )
# _pet_parser.add_argument(
#     "type", type=str, required=True, help=BLANK_ERROR.format("Pet type"), location='json'
# )
# _pet_parser.add_argument(
#     "breed", type=str, required=True, help=BLANK_ERROR.format("Pet breed"), location='json'
# )
# _pet_parser.add_argument(
#     "imageUri", type=str, required=True, help=BLANK_ERROR.format("Pet imageUri"), location='json'
# )
# _pet_parser.add_argument(
#     "disabled", type=bool, required=True, help=BLANK_ERROR.format("Disabled value"), location='json'
# )
# _pet_parser.add_argument(
#     "claws", type=list, required=True, help=BLANK_ERROR.format("Claws list"), location='json'
# )

# _claw_parser = reqparse.RequestParser()
# _claw_parser.add_argument('name', type=str, required=True, help=BLANK_ERROR.format("Claw name"), location=('message'))
# _claw_parser.add_argument('paw', type=str, required=True, help=BLANK_ERROR.format("Claw paw name"), location=('message'))
# _claw_parser.add_argument('disabled', type=bool, required=True, help=BLANK_ERROR.format("Claw disabled value"), location=('message'))
# _claw_parser.add_argument('skipped', type=bool, required=True, help=BLANK_ERROR.format("Claw skipped value"), location=('message'))
# _claw_parser.add_argument('skip_length', type=int, required=True, help=BLANK_ERROR.format("Claw skip_length value"), location=('message'))

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
    @jwt_required(refresh=True)
    def delete(cls, id: int):
        user_id = get_jwt_identity()

        pet = PetModel.find_one_by_user_id(id, user_id)

        # TODO: find all claws connected to that pet and remove them too

        if pet:
            pet.delete_from_db()
            return {"message": PET_DELETED}, 200
        return {"message": PET_NOT_FOUND}, 404

    @classmethod
    @jwt_required(refresh=True)
    def put(cls, id: int):
        pet_json = request.get_json()
        user_id = get_jwt_identity()

        pet = PetModel.find_one_by_user_id(id, user_id)
        process = ""

        if pet:
            pet.name = pet_json["name"]
            pet.type = pet_json["type"]
            pet.breed = pet_json["breed"]
            pet.imageUri = pet_json["imageUri"]
            pet.disabled = pet_json["disabled"]
            # TODO: update claws data
            pet.updated_at = str(datetime.utcnow())
            process = "updating"
        else:
            pet_json["user_id"] = user_id
            pet_json["created_at"] = str(datetime.utcnow())
            pet_json["updated_at"] = str(datetime.utcnow())
            # TODO: insert claws data
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

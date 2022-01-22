from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from datetime import datetime
from models.pet import PetModel

BLANK_ERROR = "'{}' cannot be blank."
NAME_ALREADY_EXISTS = "A pet with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting a new pet."
PET_NOT_FOUND = "Pet not found."
PET_DELETED = "Pet deleted."

_pet_parser = reqparse.RequestParser()
_pet_parser.add_argument(
    "name", type=str, required=True, help=BLANK_ERROR.format("name"), location='json'
)
_pet_parser.add_argument(
    "type", type=str, required=True, help=BLANK_ERROR.format("type"), location='json'
)
_pet_parser.add_argument(
    "breed", type=str, required=True, help=BLANK_ERROR.format("breed"), location='json'
)
_pet_parser.add_argument(
    "imageUri", type=str, required=True, help=BLANK_ERROR.format("imageUri"), location='json'
)
_pet_parser.add_argument(
    "disabled", type=bool, required=True, help=BLANK_ERROR.format("disabled"), location='json'
)


class Pet(Resource):

    @classmethod
    @jwt_required()
    def get(cls, id: int):
        user_id = get_jwt_identity()

        pet = PetModel.find_one_by_user_id(id, user_id)
        if pet:
            return pet.json(), 200
        return {"message": PET_NOT_FOUND}, 404

    @classmethod
    @jwt_required(refresh=True)
    def delete(cls, id: int):
        user_id = get_jwt_identity()

        pet = PetModel.find_one_by_user_id(id, user_id)
        
        if pet:
            pet.delete_from_db()
            return {"message": PET_DELETED}, 200
        return {"message": PET_NOT_FOUND}, 404

    @classmethod
    @jwt_required(refresh=True)
    def put(cls, id: int):
        data = _pet_parser.parse_args()
        user_id = get_jwt_identity()

        pet = PetModel.find_one_by_user_id(id, user_id)

        if pet:
            pet.name = data["name"]
            pet.type = data["type"]
            pet.breed = data["breed"]
            pet.imageUri = data["imageUri"]
            pet.disabled = data["disabled"]
            pet.updated_at = datetime.now()
        else:
            pet = PetModel(
                user_id,
                **data,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

        pet.save_to_db()

        return pet.json(), 200


class PetCreate(Resource):

    @classmethod
    @jwt_required()
    def post(cls):
        data = _pet_parser.parse_args()
        user_id = get_jwt_identity()

        # Should we check if Pet exist?
        # if PetModel.find_by_name(data["name"]):
        #     return {"message": NAME_ALREADY_EXISTS.format(data["name"])}, 400

        pet = PetModel(
            user_id,
            **data,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        try:
            pet.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return pet.json(), 201


class PetList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        user_id = get_jwt_identity()
        return {"pets": [pet.json() for pet in PetModel.find_all_by_user_id(user_id)]}, 200

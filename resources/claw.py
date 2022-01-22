from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
)
from models.claw import ClawModel


class ClawList(Resource):
    @classmethod
    @jwt_required()
    def get(cls, pet_id: int):
        return {"claws": [claw.json() for claw in ClawModel.find_all_by_pet_id(pet_id)]}, 200

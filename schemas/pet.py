from ma import ma
from models.pet import PetModel
from models.user import UserModel
from models.session import SessionModel
from models.claw import ClawModel
from schemas.session import SessionSchema
from schemas.claw import ClawSchema


class PetSchema(ma.SQLAlchemyAutoSchema):
    sessions = ma.Nested(SessionSchema, many=True)
    claws = ma.Nested(ClawSchema, many=True)

    class Meta:
        model = PetModel
        load_instance = True
        load_only = ("user", "sessions", "claws",)
        dump_only = ("id", "created_at", "updated_at",)
        include_fk = True

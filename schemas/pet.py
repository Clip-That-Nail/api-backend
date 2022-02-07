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
        load_only = ()
        dump_only = ("id", "user", "sessions",)
        include_fk = True # TODO: probably I need to remove that and use instead just ma.Nested with db.ForeignKey in the model

from ma import ma
from models.user import UserModel
from models.group import GroupModel
from models.pet import PetModel
from models.session import SessionModel
from schemas.pet import PetSchema
from schemas.session import SessionSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    pets = ma.Nested(PetSchema, many=True)
    sessions = ma.Nested(SessionSchema, many=True)

    class Meta:
        model = UserModel
        load_instance = True
        load_only = ("password", "group", "pets", "sessions",)
        dump_only = ("id", "created_at", "updated_at",)
        include_fk = True

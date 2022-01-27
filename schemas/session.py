from ma import ma
from models.session import SessionModel
from models.session_data import SessionDataModel
from schemas.session_data import SessionDataSchema


class SessionSchema(ma.SQLAlchemyAutoSchema):
    session_data = ma.Nested(SessionDataSchema, many=True)

    class Meta:
        model = SessionModel
        load_instance = True
        load_only = ()
        dump_only = ("id", "user", "pet", "session_data",)
        include_fk = True

from ma import ma
from models.session_data import SessionDataModel
from models.session import SessionModel


class SessionDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SessionDataModel
        load_instance = True
        load_only = ()
        dump_only = ("id", "session",)
        include_fk = True

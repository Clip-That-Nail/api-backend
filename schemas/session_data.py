from ma import ma
from models.session_data import SessionDataModel
from models.session import SessionModel


class SessionDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SessionDataModel
        load_instance = True
        load_only = ("session",)
        dump_only = ("id", "created_at", "updated_at",)
        include_fk = True

from ma import ma
from models.group import GroupModel
from models.user import UserModel # just to load user
from schemas.user import UserSchema


class GroupSchema(ma.SQLAlchemyAutoSchema):
    users = ma.Nested(UserSchema, many=True)

    class Meta:
        model = GroupModel
        load_instance = True
        # load_only = ()
        dump_only = ("id",)
        include_fk = True

from ma import ma
from models.claw import ClawModel
from models.pet import PetModel


class ClawSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClawModel
        load_instance = True
        load_only = ("pet",)
        dump_only = ("id", "created_at", "updated_at",)
        include_fk = True

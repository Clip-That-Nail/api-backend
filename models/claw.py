from typing import Dict, List, Union

from db import db

ClawJSON = Dict[str, Union[int, str, bool]]


class ClawModel(db.Model):
    __tablename__ = "claws"

    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    paw = db.Column(db.String(80), nullable=False)
    disabled = db.Column(db.Boolean, default=False, nullable=False)
    skipped = db.Column(db.Boolean, default=False, nullable=False)
    skip_length = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, pet_id: int, name: str, paw: str, disabled: bool, skipped: bool, skip_length: int, created_at: str, updated_at: str):
        self.pet_id = pet_id
        self.name = name
        self.paw = paw
        self.disabled = disabled
        self.skipped = skipped
        self.skip_length = skip_length
        self.created_at = created_at
        self.updated_at = updated_at

    def json(self) -> ClawJSON:
        return {
            "id": self.id,
            "pet_id": self.pet_id,
            "name": self.name,
            "paw": self.paw,
            "disabled": self.disabled,
            "skipped": self.skipped,
            "skip_length": self.skip_length,
            "created_at": self.created_at.__str__(),
            "updated_at": self.updated_at.__str__(),
        }

    @classmethod
    def find_by_id(cls, _id: int) -> "ClawModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ClawModel"]:
        return cls.query.all()

    @classmethod
    def find_all_by_pet_id(cls, pet_id: int) -> List["ClawModel"]:
        return cls.query.filter_by(pet_id=pet_id).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

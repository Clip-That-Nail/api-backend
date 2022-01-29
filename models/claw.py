from typing import List

from db import db


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
    # db.UniqueConstraint

    @classmethod
    def find_by_id(cls, _id: int) -> "ClawModel":
        return cls.query.filter_by(id=_id).first()
        
    @classmethod
    def find_one_by_pet_id_and_name(cls, pet_id: int, name: str, paw: str) -> "ClawModel":
        return cls.query.filter_by(pet_id=pet_id, name=name, paw=paw).first()

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

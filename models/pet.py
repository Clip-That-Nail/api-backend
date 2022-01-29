from typing import List

from db import db


class PetModel(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(80), nullable=False)
    image_uri = db.Column(db.String(80), nullable=False)
    disabled = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    sessions = db.relationship('SessionModel', backref='pet', lazy=True)
    claws = db.relationship('ClawModel', backref='pet', lazy=True)

    @classmethod
    def find_by_name(cls, name: str) -> "PetModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "PetModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["PetModel"]:
        return cls.query.all()

    @classmethod
    def find_all_by_user_id(cls, user_id: int) -> List["PetModel"]:
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_one_by_user_id(cls, _id: int, user_id: int) -> "PetModel":
        return cls.query.filter_by(id=_id, user_id=user_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

from typing import Dict, List, Union

from db import db

PetJSON = Dict[str, Union[int, str, bool]]


class PetModel(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(80), nullable=False)
    imageUri = db.Column(db.String(80), nullable=False)
    disabled = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    sessions = db.relationship('SessionModel', backref='pet', lazy=True)
    disabilities = db.relationship('DisabilityModel', backref='pet', lazy=True)
    skips = db.relationship('SkipModel', backref='pet', lazy=True)

    def __init__(self, user_id: int, name: str, type: str, breed: str, imageUri: str, disabled: bool, created_at: str, updated_at: str):
        self.user_id = user_id
        self.name = name
        self.type = type
        self.breed = breed
        self.imageUri = imageUri
        self.disabled = disabled
        self.created_at = created_at
        self.updated_at = updated_at

    def json(self) -> PetJSON:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "type": self.type,
            "breed": self.breed,
            "imageUri": self.imageUri,
            "disabled": self.disabled,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

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

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

from typing import Dict, List, Union

from db import db

SessionJSON = Dict[str, Union[int, str]]


class SessionModel(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pet.id"), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    session_data = db.relationship(
        'SessionDataModel', backref='session', lazy=True)

    def __init__(self, user_id: int, pet_id: int, status: str, created_at: str, updated_at: str):
        self.user_id = user_id
        self.pet_id = pet_id
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def json(self) -> SessionJSON:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "pet_id": self.pet_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def find_by_id(cls, _id: int) -> "SessionModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["SessionModel"]:
        return cls.query.all()

    @classmethod
    def find_all_by_user_id(cls, user_id: int) -> List["SessionModel"]:
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_all_by_pet_id(cls, pet_id: int) -> List["SessionModel"]:
        return cls.query.filter_by(pet_id=pet_id).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

from typing import List

from db import db


class SessionModel(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    session_data = db.relationship(
        'SessionDataModel', backref='session', lazy=True)

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

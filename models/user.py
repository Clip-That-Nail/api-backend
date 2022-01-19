from typing import Dict, Union

from db import db
from werkzeug.security import generate_password_hash

UserJSON = Dict[str, Union[int, str, bool]]


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80))
    must_change_password = db.Column(db.Boolean, default=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    pets = db.relationship('PetModel', backref='user', lazy=True)
    sessions = db.relationship('SessionModel', backref='user', lazy=True)

    def __init__(self, group_id: int, first_name: str, last_name: str, email: str, password: str, must_change_password: bool, status: int, created_at: str, updated_at: str):
        self.group_id = group_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.must_change_password = must_change_password
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def json(self) -> UserJSON:
        return {
            "id": self.id,
            "group_id": self.group_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "must_change_password": self.must_change_password,
            "status": self.status,
            "created_at": self.created_at.__str__(),
            "updated_at": self.updated_at.__str__()
        }

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

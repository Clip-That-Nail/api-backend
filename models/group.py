from typing import Dict, Union

from db import db

GroupJSON = Dict[str, Union[int, str]]


class GroupModel(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    users = db.relationship('UserModel', backref='group', lazy=True)

    def __init__(self, name: str, created_at: str, updated_at: str):
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    def json(self) -> GroupJSON:
        return {"id": self.id, "name": self.name, "created_at": self.created_at, "updated_at": self.updated_at}

    @classmethod
    def find_by_name(cls, name: str) -> "GroupModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "GroupModel":
        return cls.query.filter_by(id=_id).first()
        
    @classmethod
    def find_all(cls) -> "GroupModel":
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

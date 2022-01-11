from typing import Dict, List, Union

from db import db

ItemJSON = Dict[str, Union[int, str, float]]


class PetModel(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    # price = db.Column(db.Float(precision=2))

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("UserModel", back_populates="pet")

    def __init__(self, name: str, price: float, user_id: int):
        self.name = name
        self.price = price
        self.user_id = user_id

    def json(self) -> ItemJSON:
        return {
            "id": self.id,
            "name": self.name,
            # "price": self.price,
            "user_id": self.user_id,
        }

    @classmethod
    def find_by_name(cls, name: str) -> "PetModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["PetModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

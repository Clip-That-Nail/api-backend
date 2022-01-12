from typing import Dict, List, Union

from db import db

SessionDataJSON = Dict[str, Union[int, str]]


class SessionDataModel(db.Model):
    __tablename__ = "session_data"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey(
        "session.id"), nullable=False)
    paw = db.Column(db.String(80), nullable=False)
    claw = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    outcome = db.Column(db.String(80), nullable=False)
    behaviour = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, session_id: int, paw: str, claw: str, status: str, outcome: str, behaviour: str, created_at: str, updated_at: str):
        self.session_id = session_id
        self.paw = paw
        self.claw = claw
        self.status = status
        self.outcome = outcome
        self.behaviour = behaviour
        self.created_at = created_at
        self.updated_at = updated_at

    def json(self) -> SessionDataJSON:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "paw": self.paw,
            "claw": self.claw,
            "status": self.status,
            "outcome": self.outcome,
            "behaviour": self.behaviour,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def find_by_id(cls, _id: int) -> "SessionDataModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["SessionDataModel"]:
        return cls.query.all()

    @classmethod
    def find_all_by_session_id(cls, session_id: int) -> List["SessionDataModel"]:
        return cls.query.filter_by(session_id=session_id).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

from typing import List

from db import db


class SessionDataModel(db.Model):
    __tablename__ = "session_data"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey(
        "sessions.id"), nullable=False)
    paw = db.Column(db.String(80), nullable=False)
    claw = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    outcome = db.Column(db.String(80), nullable=False)
    behaviour = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    @classmethod
    def find_by_id(cls, _id: int) -> "SessionDataModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_one_by_session_id_and_claw(cls, session_id: int, paw: str, claw: str) -> "SessionDataModel":
        return cls.query.filter_by(session_id=session_id, paw=paw, claw=claw).first()

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

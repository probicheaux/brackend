from abc import ABC
from sqlalchemy.orm import Session
from brackend.db.models import (
    EngineGetter,
    Bracket,
)


class BracketRepository(ABC):
    engine = EngineGetter.get_or_create_engine()

    @classmethod
    def create(cls, data):
        with Session(cls.engine) as session:
            session.expire_on_commit = False
            new_bracket = Bracket(
                name=data.get("name"),
                tournament=data.get("tournament"),
                # TODO: rounds = ???
            )
            session.add(new_bracket)
            session.commit()
            return new_bracket

    @classmethod
    def delete(cls, bracket_id):
        with Session(cls.engine) as session:
            session.expire_on_commit = False
            deleted = session.query(Bracket)\
                .filter(id == bracket_id)\
                .delete()
            return deleted

    @classmethod
    def get_by_id(cls, bracket_id):
        with Session(cls.engine) as session:
            bracket = session.query(Bracket)\
                .filter(id == bracket_id)\
                .one_or_none()
            return bracket


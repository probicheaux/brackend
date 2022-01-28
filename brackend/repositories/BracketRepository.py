from abc import ABC
from sqlalchemy.orm import Session, subqueryload
from brackend.db.models import (
    EngineGetter,
    Bracket,
    UserTournament,
    User,
)
from brackend.db.enums import UserRole
from brackend.util import BrackendException


class BracketRepository(ABC):
    engine = EngineGetter.get_or_create_engine()

    @classmethod
    def create(cls, data):
        with Session(cls.engine) as session:
            session.expire_on_commit = False
            new_bracket = Bracket(
                name=data.get("name"),
                tournament=data.get("tournament"),
                description=data.get("description"),
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
                .filter(Bracket.id == bracket_id)\
                .delete()
            return deleted

    @classmethod
    def get_by_id(cls, bracket_id):
        with Session(cls.engine) as session:
            bracket = session.query(Bracket)\
                .filter(Bracket.id == bracket_id)\
                .one_or_none()
            return bracket

    @classmethod
    def get_participants(cls, bracket_id):
        with Session(cls.engine) as session:
            participants = session.query(User) \
                .join(UserTournament, User.id == UserTournament.user_id) \
                .filter(UserTournament.bracket_id == bracket_id)\
                .all()
            return participants

    @classmethod
    def check_has_joined(cls, bracket_id, user):
        with Session(cls.engine) as session:
            existing = session.query(UserTournament)\
                .filter(
                    UserTournament.user_id == user.id,
                    UserTournament.bracket_id == bracket_id,
                ).one_or_none()
            return existing is not None

    @classmethod
    def join_bracket(cls, bracket_id, user, join_role=UserRole.player):
        with Session(cls.engine) as session:
            session.expire_on_commit = False
            bracket = session.query(Bracket) \
                .filter(Bracket.id == bracket_id).one_or_none()
            if bracket is None:
                raise BrackendException("Bracket not found")
            entry = UserTournament(
                user_id=user.id,
                tournament_id=bracket.tournament,
                bracket_id=bracket_id,
                role=join_role
            )
            session.add(entry)
            session.commit()

            return entry


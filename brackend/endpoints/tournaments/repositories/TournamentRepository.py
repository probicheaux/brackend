from abc import ABC
from sqlalchemy.orm import Session
from brackend.db.models import (
    EngineGetter,
    Tournament,
    UserTournament,
    User,
)
from brackend.db.enums import UserRole


class TournamentRepository(ABC):
    engine = EngineGetter.get_or_create_engine()

    @classmethod
    def get_by_id(cls, t_id):
        """
            Return a tournament with it's owner info
        """
        with Session(cls.engine) as session:
            result = session.query(Tournament, User)\
                .join(UserTournament, Tournament.id == UserTournament.tournament_id)\
                .join(User.id == UserTournament.user_id)\
                .filter(Tournament.id == t_id)\
                .filter(UserTournament.role == UserRole.organizer)\
                .all()

            return {
                **result.Tournanment,
                "owner": result.User
            }

    @classmethod
    def search_by_name(cls, name, count=20):
        with Session(cls.engine) as session:
            search = "%{}%".format(name)
            results = session.query(Tournament)\
                .filter(Tournament.name.like(search))\
                .limit(count)\
                .all()
            return results



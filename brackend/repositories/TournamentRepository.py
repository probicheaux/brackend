from abc import ABC
from sqlalchemy.orm import Session, subqueryload
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
    def get_all_for_user(cls, user):
        with Session(cls.engine) as session:
            tournaments = session.query(Tournament) \
                .options(subqueryload(Tournament.brackets)) \
                .join(Tournament.user_tournaments) \
                .where(UserTournament.user_id == user.id) \
                .all()

            return tournaments

    @classmethod
    def get_by_id(cls, t_id):
        """
            Return a tournament with it's owner info
        """
        with Session(cls.engine) as session:
            result = session.query(Tournament, User) \
                .options(subqueryload(Tournament.brackets)) \
                .join(UserTournament, Tournament.id == UserTournament.tournament_id) \
                .join(User, User.id == UserTournament.user_id) \
                .filter(Tournament.id == t_id) \
                .filter(UserTournament.role == UserRole.organizer) \
                .all()

            tournament = result[0][0]
            owner = result[0][1]

            tournament.add_owner_info(owner)

            return tournament

    @classmethod
    def search_by_name(cls, name, count=20):
        with Session(cls.engine) as session:
            search = "%{}%".format(name)
            results = session.query(Tournament) \
                .options(subqueryload(Tournament.brackets)) \
                .filter(Tournament.name.ilike(search))\
                .limit(count)\
                .all()
            return results



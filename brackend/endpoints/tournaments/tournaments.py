from flask import Blueprint, current_app, jsonify, request, g
from flask_restful import Api, Resource

from brackend.tasks.auth import requires_auth
from brackend.tasks.tasks import get_tournament_by_id, save_new_tournament, get_tournaments_by_uid
from brackend.endpoints.tournaments.repositories.TournamentRepository import TournamentRepository

tournament_bp = Blueprint("tournaments", __name__)
tournament_api = Api(tournament_bp)


@requires_auth
class Tournaments(Resource):
    """Create a new tournament."""

    def post(self):
        body = request.get_json()
        name = body.get("name")
        new_tourny = save_new_tournament(name, g.firebase_id)
        return jsonify(new_tourny.to_json())

    def get(self):
        tourneys = get_tournaments_by_uid(g.firebase_id)
        return jsonify(tournaments=[tournament.to_json() for tournament in tourneys])


@requires_auth
class TournamentDetails(Resource):
    """Get info for specific tournament, by id."""

    def get(self, tournament_id):
        tourny = get_tournament_by_id(tournament_id)
        return jsonify(tourny.to_json())


@requires_auth
class TournamentSearch(Resource):
    """Get info for specific tournament, by id."""

    def post(self):
        body = request.get_json()
        name = body.get("name")
        # TODO: Eventually search by short id code
        results = TournamentRepository.search_by_name(name)
        return jsonify(results=[result.to_json() for result in results])


tournament_api.add_resource(Tournaments, "/tournaments")
tournament_api.add_resource(TournamentSearch, "/tournaments/search")
tournament_api.add_resource(TournamentDetails, "/tournaments/<string:tournament_id>")

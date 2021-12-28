from flask import Blueprint, current_app, jsonify, request
from flask_restful import Api, Resource

from brackend.tasks.auth import requires_auth
from brackend.tasks.tasks import get_tournament_by_id, save_new_tournament, get_tournaments_by_uid

tournament_bp = Blueprint("tournaments", __name__)
tournament_api = Api(tournament_bp)


@requires_auth
class Tournaments(Resource):
    """Create a new tournament."""

    def post(self, firebase_id):
        body = request.get_json()
        name = body.get("name")
        new_tourny = save_new_tournament(name, firebase_id)
        return jsonify(new_tourny.to_json())

    def get(self, firebase_id):
        tourneys = get_tournaments_by_uid(firebase_id)
        return jsonify(tournaments=[tournament.to_json() for tournament in tourneys])


@requires_auth
class TournamentDetails(Resource):
    """Get info for specific tournament, by id."""

    def get(self, firebase_id, tournament_id):
        tourny = get_tournament_by_id(tournament_id)
        return jsonify(tourny.to_json())


tournament_api.add_resource(Tournaments, "/tournaments")
tournament_api.add_resource(TournamentDetails, "/tournaments/<string:tournament_id>")

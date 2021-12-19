from flask import Blueprint, request, jsonify

from flask_restful import Api
from flask_restful import Resource

from brackend.tasks.tasks import (
    save_new_tournament,
    get_tournament_by_id,
)

tournament_bp = Blueprint('tournaments', __name__)
tournament_api = Api(tournament_bp)


class Tournaments(Resource):
    """
        Create a new tournament
    """
    def post(self):
        body = request.get_json()
        name = body.get("name")
        new_tourny = save_new_tournament(name)
        return jsonify(new_tourny)


class TournamentDetails(Resource):
    """
        Get info for specific tournament, by id
    """
    def get(self, tournament_id):
        tourny = get_tournament_by_id(tournament_id)
        return jsonify(tourny)


tournament_api.add_resource(Tournaments, '/tournaments')
tournament_api.add_resource(TournamentDetails, '/tournaments/<string:tournament_id>')
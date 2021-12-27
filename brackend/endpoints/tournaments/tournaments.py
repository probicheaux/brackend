from flask import Blueprint, current_app, jsonify, request
from flask_restful import Api, Resource

from brackend.tasks.auth import auth_decorator
from brackend.tasks.tasks import get_tournament_by_id, save_new_tournament

tournament_bp = Blueprint("tournaments", __name__)
tournament_api = Api(tournament_bp)


class Tournaments(Resource):
    """Create a new tournament."""

    method_decorators = [auth_decorator]

    def post(self, firebase_id):
        body = request.get_json()
        current_app.logger.info(firebase_id)
        name = body.get("name")
        new_tourny = save_new_tournament(name, firebase_id)
        return jsonify(new_tourny.to_json())


class TournamentDetails(Resource):
    """Get info for specific tournament, by id."""

    method_decorators = [auth_decorator]

    def get(self, firebase_id, tournament_id):
        current_app.logger.info(firebase_id)
        tourny = get_tournament_by_id(tournament_id)
        return jsonify(tourny.to_json())


tournament_api.add_resource(Tournaments, "/tournaments")
tournament_api.add_resource(TournamentDetails, "/tournaments/<string:tournament_id>")

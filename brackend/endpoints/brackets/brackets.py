from flask import Blueprint, jsonify, request, g
from flask_restful import Api, Resource

from brackend.tasks.auth import requires_auth
from brackend.util import BrackendException
from brackend.endpoints.tournaments.repositories.TournamentRepository import TournamentRepository
from brackend.endpoints.brackets.repositories.BracketRepository import BracketRepository

brackets_bp = Blueprint("brackets", __name__)
brackets_api = Api(brackets_bp)

@requires_auth
class Brackets(Resource):
    """Add a new bracket to an existing tournament."""

    def post(self):
        body = request.get_json()
        tournament_id = body.get("tournament")

        # Validate that this user owns the tournament they are attempting to add a bracket to
        tournament, owner = TournamentRepository.get_by_id_with_owner(tournament_id)
        if g.user.id != owner.id:
            raise BrackendException("Tournament does not belong to user")
        data = {
            "tournament": body.get("tournament"),
            "name": body.get("name"),
        }
        new_bracket = BracketRepository.create(data)
        return jsonify(new_bracket.to_json())


@requires_auth
class BracketDetails(Resource):

    def delete(self, bracket_id):
        bracket = BracketRepository.get_by_id(bracket_id)
        tournament, owner = TournamentRepository.get_by_id_with_owner(bracket.tournament)
        if g.user.id != owner.id:
            raise BrackendException("Tournament does not belong to user")
        deleted = BracketRepository.delete(bracket_id)
        return jsonify(deleted.to_json())


brackets_api.add_resource(Brackets, "/brackets")
brackets_api.add_resource(BracketDetails, "/brackets/<string:bracket_id>")

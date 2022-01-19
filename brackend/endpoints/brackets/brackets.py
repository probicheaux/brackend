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
        tournament = TournamentRepository.get_by_id(tournament_id)
        if g.user.id != tournament.owner.id:
            raise BrackendException("Tournament does not belong to user")
        data = {
            "tournament": body.get("tournament"),
            "name": body.get("name"),
        }
        new_bracket = BracketRepository.create(data)
        return jsonify(new_bracket.to_json())


@requires_auth
class BracketDetails(Resource):

    def get(self, bracket_id):
        bracket = BracketRepository.get_by_id(bracket_id)
        participants = BracketRepository.get_participants(bracket_id)
        return jsonify(bracket.to_json(participants=[p.to_json() for p in participants]))

    def delete(self, bracket_id):
        bracket = BracketRepository.get_by_id(bracket_id)
        tournament = TournamentRepository.get_by_id(bracket.tournament)
        if g.user.id != tournament.owner.id:
            raise BrackendException("Tournament does not belong to user")
        deleted = BracketRepository.delete(bracket_id)
        return jsonify(deleted.to_json())

@requires_auth
class BracketJoin(Resource):
    def post(self, bracket_id):
        has_joined = BracketRepository.check_has_joined(
            bracket_id=bracket_id,
            user=g.user,
        )
        if has_joined:
            return {"message": "User has already joined this bracket"}, 200
        BracketRepository.join_bracket(bracket_id=bracket_id, user=g.user)
        return {"message": "Joined tournament"}


brackets_api.add_resource(Brackets, "/brackets")
brackets_api.add_resource(BracketDetails, "/brackets/<string:bracket_id>")
brackets_api.add_resource(BracketJoin, "/brackets/<string:bracket_id>/join")

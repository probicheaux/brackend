from flask import Blueprint, current_app, jsonify, request
from flask_restful import Api, Resource, abort

from brackend.tasks.auth import requires_auth
from brackend.tasks.tasks import get_user_by_uid, save_new_user

users_bp = Blueprint("users", __name__)
users_api = Api(users_bp)


@requires_auth
class Users(Resource):
    """Create a new user from a firebase user."""

    def post(self, firebase_id):
        body = request.get_json()
        username = body.get("username")
        new_user = save_new_user(username, firebase_id)
        return jsonify(new_user.to_json())

    def get(self, firebase_id):
        user = get_user_by_uid(firebase_id)
        if user is None:
            abort(404, message=f"User with id {firebase_id} not found")

        return jsonify(user.to_json())

@requires_auth
class UserDetails(Resource):
    """Get info for specific tournament, by id."""

    def get(self, firebase_id, user_id):
        user = get_user_by_uid(user_id)
        return jsonify(user.to_json())

users_api.add_resource(Users, "/users")
users_api.add_resource(UserDetails, "/users/<string:user_id>")

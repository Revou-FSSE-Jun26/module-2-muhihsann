from flask import Blueprint, request, jsonify
from app import db
from app.models import User

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["POST"])
def register_user():
    """Register a new user."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    username = data.get("username")
    email = data.get("email")
    password_hash = data.get("password_hash")

    if not username or not email or not password_hash:
        return jsonify({"error": "username, email, and password_hash are required"}), 400

    # Check for existing username or email
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    try:
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Get a specific user."""
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

from flask import Blueprint, request, jsonify
from app import db
from app.models import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["POST"])
def register_user():
    data = request.get_json()

    if not data or not all(k in data for k in ("username", "email", "password_hash")):
        return jsonify({"error": "username, email, and password_hash are required"}), 400

    role = data.get("role", "customer")
    if role not in ("customer", "seller"):
        return jsonify({"error": "role must be 'customer' or 'seller'"}), 400

    new_user = User(
        username=data["username"],
        email=data["email"],
        password_hash=data["password_hash"],
        role=role,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200
from flask import Blueprint, request, jsonify
from app.models import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    """Login a user by verifying username/email and password_hash."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    email = data.get("email")
    password_hash = data.get("password_hash")

    if not email or not password_hash:
        return jsonify({"error": "email and password_hash are required"}), 400

    user = User.query.filter_by(email=email).first()

    if user is None or user.password_hash != password_hash:
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": user.to_dict()
    }), 200

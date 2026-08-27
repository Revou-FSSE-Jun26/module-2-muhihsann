from flask import Blueprint, request, jsonify
from app import db
from app.models import Category, Product

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/categories", methods=["GET"])
def list_categories():
    """List all categories."""
    categories = Category.query.all()
    result = []
    for c in categories:
        result.append({
            "id": c.id,
            "name": c.name,
            "description": c.description,
        })
    return jsonify(result), 200


@categories_bp.route("/categories/<int:category_id>", methods=["GET"])
def get_category(category_id):
    """Get a specific category along with its products."""
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({"error": "Category not found"}), 404

    products = []
    for p in category.products:
        products.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "stock_quantity": p.stock_quantity,
            "category_id": p.category_id,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        })

    return jsonify({
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "products": products,
    }), 200


@categories_bp.route("/categories", methods=["POST"])
def create_category():
    """Create a new category."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    name = data.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400

    # Check for duplicate name
    if Category.query.filter_by(name=name).first():
        return jsonify({"error": "Category name already exists"}), 409

    try:
        category = Category(
            name=name,
            description=data.get("description"),
        )
        db.session.add(category)
        db.session.commit()
        return jsonify({
            "id": category.id,
            "name": category.name,
            "description": category.description,
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@categories_bp.route("/categories/<int:category_id>", methods=["PUT"])
def update_category(category_id):
    """Update an existing category."""
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({"error": "Category not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "name" in data:
        if not data["name"]:
            return jsonify({"error": "name cannot be empty"}), 400
        # Check duplicate name (exclude current category)
        existing = Category.query.filter_by(name=data["name"]).first()
        if existing and existing.id != category_id:
            return jsonify({"error": "Category name already exists"}), 409
        category.name = data["name"]

    if "description" in data:
        category.description = data["description"]

    try:
        db.session.commit()
        return jsonify({
            "id": category.id,
            "name": category.name,
            "description": category.description,
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@categories_bp.route("/categories/<int:category_id>", methods=["DELETE"])
def delete_category(category_id):
    """Delete a category."""
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({"error": "Category not found"}), 404

    # Check if category has products
    if Product.query.filter_by(category_id=category_id).first():
        return jsonify({"error": "Cannot delete category that has products"}), 400

    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "Category deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

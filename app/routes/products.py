from flask import Blueprint, request, jsonify
from app import db
from app.models import Product, Category, Order, order_items

products_bp = Blueprint("products", __name__)


@products_bp.route("/products", methods=["GET"])
def list_products():
    """List all products."""
    products = Product.query.all()
    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "stock_quantity": p.stock_quantity,
            "category_id": p.category_id,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        })
    return jsonify(result), 200


@products_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Get a specific product."""
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock_quantity": product.stock_quantity,
        "category_id": product.category_id,
        "created_at": product.created_at.isoformat() if product.created_at else None,
    }), 200


@products_bp.route("/products", methods=["POST"])
def create_product():
    """Create a new product with validation."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    # Validate required fields
    name = data.get("name")
    price = data.get("price")
    category_id = data.get("category_id")

    if not name:
        return jsonify({"error": "name is required"}), 400
    if price is None:
        return jsonify({"error": "price is required"}), 400
    if category_id is None:
        return jsonify({"error": "category_id is required"}), 400

    # Validate types
    if not isinstance(price, (int, float)) or price < 0:
        return jsonify({"error": "price must be a non-negative number"}), 400

    stock_quantity = data.get("stock_quantity", 0)
    if not isinstance(stock_quantity, int) or stock_quantity < 0:
        return jsonify({"error": "stock_quantity must be a non-negative integer"}), 400

    # Validate category exists
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({"error": "Category not found"}), 404

    try:
        product = Product(
            name=name,
            description=data.get("description"),
            price=int(price),
            stock_quantity=stock_quantity,
            category_id=category_id,
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock_quantity": product.stock_quantity,
            "category_id": product.category_id,
            "created_at": product.created_at.isoformat() if product.created_at else None,
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@products_bp.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Update an existing product with validation."""
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    # Validate fields if provided
    if "name" in data:
        if not data["name"]:
            return jsonify({"error": "name cannot be empty"}), 400
        product.name = data["name"]

    if "description" in data:
        product.description = data["description"]

    if "price" in data:
        price = data["price"]
        if not isinstance(price, (int, float)) or price < 0:
            return jsonify({"error": "price must be a non-negative number"}), 400
        product.price = int(price)

    if "stock_quantity" in data:
        stock_quantity = data["stock_quantity"]
        if not isinstance(stock_quantity, int) or stock_quantity < 0:
            return jsonify({"error": "stock_quantity must be a non-negative integer"}), 400
        product.stock_quantity = stock_quantity

    if "category_id" in data:
        category = Category.query.get(data["category_id"])
        if category is None:
            return jsonify({"error": "Category not found"}), 404
        product.category_id = data["category_id"]

    try:
        db.session.commit()
        return jsonify({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock_quantity": product.stock_quantity,
            "category_id": product.category_id,
            "created_at": product.created_at.isoformat() if product.created_at else None,
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@products_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a product. Blocked if active orders exist."""
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    # Check if product has active orders (not delivered or cancelled)
    active_statuses = ("pending", "processing", "shipped")
    active_order_count = (
        db.session.query(Order)
        .join(order_items, Order.id == order_items.c.order_id)
        .filter(order_items.c.product_id == product_id)
        .filter(Order.status.in_(active_statuses))
        .count()
    )

    if active_order_count > 0:
        return jsonify({
            "error": "Cannot delete product with active orders"
        }), 400

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

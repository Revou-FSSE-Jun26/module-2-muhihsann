from flask import Blueprint, jsonify

products_bp = Blueprint("products", __name__)

# Hardcoded for now — real DB-backed version comes in Checkpoint 3
HARDCODED_PRODUCTS = [
    {"id": 1, "name": "Wireless Mouse", "price": 20},
    {"id": 2, "name": "Mechanical Keyboard", "price": 90},
    {"id": 3, "name": "Stainless Steel Pan", "price": 35},
    {"id": 4, "name": "Espresso Machine", "price": 199},
]

@products_bp.route("/products", methods=["GET"])
def list_products():
    return jsonify(HARDCODED_PRODUCTS), 200

@products_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in HARDCODED_PRODUCTS if p["id"] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200
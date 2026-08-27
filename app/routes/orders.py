from flask import Blueprint, request, jsonify
from app import db
from app.models import Order, Product, User, order_items

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders", methods=["POST"])
def create_order():
    """Place a new order linked to a user (user_id in body)."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    user_id = data.get("user_id")
    items = data.get("items")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    if not items or not isinstance(items, list) or len(items) == 0:
        return jsonify({"error": "items is required and must be a non-empty list"}), 400

    # Validate user exists
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    # Validate each item and calculate total
    total_amount = 0
    order_item_rows = []

    for item in items:
        product_id = item.get("product_id")
        quantity = item.get("quantity", 1)

        if not product_id:
            return jsonify({"error": "Each item must have a product_id"}), 400
        if not isinstance(quantity, int) or quantity <= 0:
            return jsonify({"error": "quantity must be a positive integer"}), 400

        product = Product.query.get(product_id)
        if product is None:
            return jsonify({"error": f"Product with id {product_id} not found"}), 404

        # Check stock
        if product.stock_quantity < quantity:
            return jsonify({
                "error": f"Insufficient stock for product '{product.name}'. Available: {product.stock_quantity}"
            }), 400

        unit_price = product.price
        total_amount += unit_price * quantity
        order_item_rows.append({
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price,
        })

    try:
        # Create order
        order = Order(
            user_id=user_id,
            status="pending",
            total_amount=total_amount,
        )
        db.session.add(order)
        db.session.flush()  # get order.id

        # Insert order items and reduce stock
        for row in order_item_rows:
            db.session.execute(order_items.insert().values(
                order_id=order.id,
                product_id=row["product_id"],
                quantity=row["quantity"],
                unit_price=row["unit_price"],
            ))
            # Reduce stock
            product = Product.query.get(row["product_id"])
            product.stock_quantity -= row["quantity"]

        db.session.commit()

        return jsonify({
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "total_amount": order.total_amount,
            "order_date": order.order_date.isoformat() if order.order_date else None,
            "items": order_item_rows,
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@orders_bp.route("/orders", methods=["GET"])
def list_orders():
    """List all orders for a user (user_id as query param)."""
    user_id = request.args.get("user_id", type=int)

    if not user_id:
        return jsonify({"error": "user_id query parameter is required"}), 400

    orders = Order.query.filter_by(user_id=user_id).all()
    result = []
    for o in orders:
        result.append({
            "id": o.id,
            "user_id": o.user_id,
            "status": o.status,
            "total_amount": o.total_amount,
            "order_date": o.order_date.isoformat() if o.order_date else None,
        })
    return jsonify(result), 200


@orders_bp.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """View a specific order with its order items and product details."""
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404

    # Fetch order items with product details
    items_query = (
        db.session.query(
            order_items.c.product_id,
            order_items.c.quantity,
            order_items.c.unit_price,
            Product.name.label("product_name"),
        )
        .join(Product, Product.id == order_items.c.product_id)
        .filter(order_items.c.order_id == order_id)
        .all()
    )

    items = []
    for row in items_query:
        items.append({
            "product_id": row.product_id,
            "product_name": row.product_name,
            "quantity": row.quantity,
            "unit_price": row.unit_price,
        })

    return jsonify({
        "id": order.id,
        "user_id": order.user_id,
        "status": order.status,
        "total_amount": order.total_amount,
        "order_date": order.order_date.isoformat() if order.order_date else None,
        "items": items,
    }), 200


@orders_bp.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    """Update an existing order (e.g. change status)."""
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if "status" in data:
        valid_statuses = ("pending", "processing", "shipped", "delivered", "cancelled")
        if data["status"] not in valid_statuses:
            return jsonify({"error": f"status must be one of: {', '.join(valid_statuses)}"}), 400
        order.status = data["status"]

    try:
        db.session.commit()
        return jsonify({
            "id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "total_amount": order.total_amount,
            "order_date": order.order_date.isoformat() if order.order_date else None,
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@orders_bp.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    """Delete an order."""
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404

    try:
        # order_items rows will be cascade-deleted by the DB (ON DELETE CASCADE)
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

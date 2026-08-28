from app import create_app, db
from app.models import Order, Product

app = create_app()

with app.app_context():
    order = Order.query.get(1)
    products = Product.query.filter(Product.id.in_([1, 2])).all()
    order.products = products
    db.session.commit()
    print(f"Order {order.id} now linked to: {[p.name for p in order.products]}")
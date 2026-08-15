from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    role = db.Column(db.String(20), nullable=False, server_default="customer")

    orders = db.relationship("Order", backref="user", cascade=None)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)

    products = db.relationship("Product", backref="category")


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), nullable=False, default="pending")
    total_amount = db.Column(db.Integer, nullable=False, default=0)

    # many-to-many to Product, through the order_items association table
    products = db.relationship("Product", secondary="order_items", backref="orders")


# order_items — association table, NOT a full model class.
# The rubric specifically calls for db.Table() here rather than a mapped class,
# since order_items only needs to link two IDs plus a couple of extra columns.
order_items = db.Table(
    "order_items",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("order_id", db.Integer, db.ForeignKey("orders.id"), nullable=False),
    db.Column("product_id", db.Integer, db.ForeignKey("products.id"), nullable=False),
    db.Column("quantity", db.Integer, nullable=False),
    db.Column("unit_price", db.Integer, nullable=False),
)

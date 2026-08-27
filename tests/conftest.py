import pytest
from app import create_app, db


@pytest.fixture
def app():
    """Create a test app with an in-memory SQLite database."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture
def seed_category(app):
    """Seed a category for tests that need one already in the DB."""
    from app.models import Category

    with app.app_context():
        category = Category(name="Electronics", description="Phones and laptops")
        db.session.add(category)
        db.session.commit()
        return {"id": category.id, "name": category.name, "description": category.description}


@pytest.fixture
def seed_category_with_product(app):
    """Seed a category that has a product (for delete-guard test)."""
    from app.models import Category, Product

    with app.app_context():
        category = Category(name="Books", description="Fiction and non-fiction")
        db.session.add(category)
        db.session.flush()
        product = Product(
            name="Test Book",
            description="A test book",
            price=15,
            stock_quantity=10,
            category_id=category.id,
        )
        db.session.add(product)
        db.session.commit()
        return {"id": category.id, "name": category.name}

"""
Test cases for Category CRUD endpoints.
Covers happy path and error cases for each endpoint.
"""


# ============================================================
# POST /categories
# ============================================================

class TestCreateCategory:
    """POST /categories"""

    def test_create_category_success(self, client):
        """Happy path: create a category with valid data."""
        response = client.post("/categories", json={
            "name": "Sportswear",
            "description": "Athletic clothing and gear"
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "Sportswear"
        assert data["description"] == "Athletic clothing and gear"
        assert "id" in data

    def test_create_category_missing_name(self, client):
        """Error: name is required."""
        response = client.post("/categories", json={
            "description": "No name provided"
        })
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_create_category_empty_body(self, client):
        """Error: empty request body."""
        response = client.post("/categories", json={})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_create_category_duplicate_name(self, client, seed_category):
        """Error: duplicate category name returns 409."""
        response = client.post("/categories", json={
            "name": "Electronics",
            "description": "Duplicate"
        })
        assert response.status_code == 409
        data = response.get_json()
        assert "error" in data


# ============================================================
# GET /categories
# ============================================================

class TestListCategories:
    """GET /categories"""

    def test_list_categories_empty(self, client):
        """Happy path: returns empty list when no categories exist."""
        response = client.get("/categories")
        assert response.status_code == 200
        data = response.get_json()
        assert data == []

    def test_list_categories_with_data(self, client, seed_category):
        """Happy path: returns list with seeded category."""
        response = client.get("/categories")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]["name"] == "Electronics"


# ============================================================
# GET /categories/<id>
# ============================================================

class TestGetCategory:
    """GET /categories/<id>"""

    def test_get_category_success(self, client, seed_category):
        """Happy path: returns category with its products."""
        response = client.get(f"/categories/{seed_category['id']}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "Electronics"
        assert "products" in data
        assert isinstance(data["products"], list)

    def test_get_category_not_found(self, client):
        """Error: non-existent category returns 404."""
        response = client.get("/categories/999")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data


# ============================================================
# PUT /categories/<id>
# ============================================================

class TestUpdateCategory:
    """PUT /categories/<id>"""

    def test_update_category_success(self, client, seed_category):
        """Happy path: update name and description."""
        response = client.put(f"/categories/{seed_category['id']}", json={
            "name": "Updated Electronics",
            "description": "Updated description"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "Updated Electronics"
        assert data["description"] == "Updated description"

    def test_update_category_not_found(self, client):
        """Error: updating non-existent category returns 404."""
        response = client.put("/categories/999", json={
            "name": "Ghost"
        })
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_update_category_empty_name(self, client, seed_category):
        """Error: empty name returns 400."""
        response = client.put(f"/categories/{seed_category['id']}", json={
            "name": ""
        })
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_update_category_empty_body(self, client, seed_category):
        """Error: empty request body returns 400."""
        response = client.put(f"/categories/{seed_category['id']}", json={})
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


# ============================================================
# DELETE /categories/<id>
# ============================================================

class TestDeleteCategory:
    """DELETE /categories/<id>"""

    def test_delete_category_success(self, client, seed_category):
        """Happy path: delete a category with no products."""
        response = client.delete(f"/categories/{seed_category['id']}")
        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data

        # Verify it's gone
        response = client.get(f"/categories/{seed_category['id']}")
        assert response.status_code == 404

    def test_delete_category_not_found(self, client):
        """Error: deleting non-existent category returns 404."""
        response = client.delete("/categories/999")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_delete_category_with_products(self, client, seed_category_with_product):
        """Error: deleting category that has products returns 400."""
        response = client.delete(f"/categories/{seed_category_with_product['id']}")
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "products" in data["error"].lower() or "product" in data["error"].lower()

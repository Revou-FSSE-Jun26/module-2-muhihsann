"""
Locust load test for RevoShop API.

Simulates a sequential user journey:
    1. GET all products
    2. GET a single product by ID
    3. POST a new order
    4. GET the created order

Run with the Flask server already running on port 5000:
    locust -f locustfile.py --host http://127.0.0.1:5000

Then open http://localhost:8089 and set:
    Number of users: 200
    Spawn rate:      10   (ramps from ~50 up to 200 gradually)
"""

from locust import HttpUser, task, between


class RevoShopUser(HttpUser):
    # Each simulated user waits 1-3 seconds between journeys
    wait_time = between(1, 3)

    @task
    def user_journey(self):
        # Step 1: GET all products
        self.client.get("/products", name="1. GET all products")

        # Step 2: GET a single product by ID
        self.client.get("/products/1", name="2. GET product by id")

        # Step 3: POST a new order
        order_payload = {
            "user_id": 1,
            "items": [
                {"product_id": 1, "quantity": 1}
            ]
        }
        with self.client.post(
            "/orders",
            json=order_payload,
            name="3. POST new order",
            catch_response=True,
        ) as response:
            if response.status_code == 201:
                response.success()
                order_id = response.json().get("id")
            elif response.status_code == 400:
                # Out of stock under heavy load is expected, not a real failure
                response.success()
                order_id = None
            else:
                response.failure(f"Unexpected status: {response.status_code}")
                order_id = None

        # Step 4: GET the created order (only if it was created)
        if order_id:
            self.client.get(f"/orders/{order_id}", name="4. GET created order")

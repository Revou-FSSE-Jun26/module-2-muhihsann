# RevoShop Database

Backend database schema for RevoShop, an online store. Built with PostgreSQL.


## Entities
Check out `img/revoshop_db.png` for the detailed server tree.
![RevoShop DB server tree](img/revoshop_db.png)
- **users** — customer accounts
- **categories** — product categories
- **products** — store items, each linked to a category
- **orders** — placed by a user
- **order_items** — junction table linking orders and products

Check out `img/erd.png` for the full schema diagram.
![ERD schema diagram](img/erd.png)


## Requirements

- PostgreSQL 16+ installed locally
- `psql` CLI available, or a GUI client such as DBeaver / pgAdmin installed locally


## Local Setup Guide

**1. Install PostgreSQL and Set the Superuser Password :**
   - Download and install PostgreSQL 16+ from [postgresql.org/download](https://www.postgresql.org/download/) 
   - During install (Windows/Mac) you'll be prompted to set a password for the `postgres` superuser — set one and remember it.

   - Verify the install :
```bash
     psql -U postgres -h localhost -c "SELECT version();"
```
If it prompts for your password and prints a version string, PostgreSQL is installed and running correctly.


**2. Connect DBeaver to PostgreSQL :**
   - Open DBeaver → **Database → New Database Connection** → select **PostgreSQL** → **Next**.
   - Host: `localhost`, Port: `5432`, Database: `postgres`, Username: `postgres`, Password: the one you set in step 1.
   - Click **Test Connection…** (DBeaver may prompt to download the PostgreSQL driver the first time — allow it), then **Finish**.


**3. Create the Database :**
```bash
   psql -U postgres -c "CREATE DATABASE revoshop_db;"
```
   (Or create it through DBeaver/pgAdmin's GUI : right-click Databases → Create New Database → name it `revoshop_db`.)


**4. Load the Schema :**
```bash
   psql -U postgres -d revoshop_db -f schema.sql
```
   (Or in DBeaver/pgAdmin's GUI : right-click `revoshop_db` → **SQL Editor → Open SQL Script**, open `schema.sql`, then run it with **Execute SQL Script**.)


**5. Load the Sample Data :**
```bash
   psql -U postgres -d revoshop_db -f seed.sql
```
   (Or in DBeaver/pgAdmin's GUI : open a new SQL editor on `revoshop_db`, open `seed.sql`, then run it with **Execute SQL Script**.)


**6. Try the Example Queries :**
```bash
   psql -U postgres -d revoshop_db -f queries.sql
```
   (Or in DBeaver/pgAdmin's GUI : open `queries.sql` in a SQL editor on `revoshop_db` and run each statement with **Ctrl+Enter**, or the whole file with **Execute SQL Script**.)


---


## Checkpoint 2 - Flask App Setup

## Project Structure

```text
revoshop-db/
├── database/
│   ├── schema.sql        # from Checkpoint 1
│   ├── seed.sql
│   └── queries.sql
├── img/
│   ├── revoshop_db.png
│   ├── erd.png
│   └── postman/           # Checkpoint 2 demo screenshots
├── app/
│   ├── __init__.py       # app factory + db init
│   ├── config.py         # SQLALCHEMY_DATABASE_URI
│   ├── models.py         # User, Category, Product, Order, order_items
│   └── routes/
│       ├── __init__.py
│       ├── products.py   # hardcoded product routes
│       └── users.py      # register/retrieve routes
├── migrations/            # created automatically by flask db init
├── run.py                 # entry point
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Setup Guide

1. Create and activate a virtual environment, then install dependencies:
```bash
   python -m venv venv

   ### MacOS and Linux :
   source venv/bin/activate

   ### Windows : 
   .\venv\Scripts\Activate.ps1
   
   pip install -r requirements.txt
```
2. Copy `.env.example` to `.env` and fill in the real PostgreSQL password. (eg.: postgres)
3. Run the migrations against your existing `revoshop_db`:
```bash
   export FLASK_APP=run.py
   flask db upgrade
```
4. Start the app:
```bash
   python run.py
```
5. Test routes via Postman or `curl`:
   - `GET /products`
   - `GET /products/<id>`
   - `POST /users`
   - `GET /users/<id>`


---

## Image Evidence 
Check out `img/` and `img/postman/` for the full evidence

**1. GET/products - List all active Products [200 OK]**
![GET all products](img/postman/GET_all_products_postman.png)

**2. GET/products/3 - List Products by the id [200 OK]**
![GET product 3](img/postman/GET_products3_postman.png)

**3. GET/products/999 - List Products by the id : [404 Not Found Case]**
![GET product 999 not found](img/postman/GET_products999_postman.png)

**4. POST/Users - Create new Users [201 Created]**
![POST new user](img/postman/POST_users5_postman.png)

**5. GET/Users/5 - List Users by the id [200 OK]**
![GET user 5](img/postman/GET_users5_postman.png)

**6. GET/Users/999 - List Users by the id : [404 Not Found Case]**
![GET user 999 not found](img/postman/GET_users999_postman.png)

**7. Added the role column to Users without affecting existing rows**
![role column added](img/added_users5_role.png)

**8. The order_items association table exists, many-to-many verification**
![many-to-many verification](img/many_to_many.png)
Order 1 is linked to two products (Wireless Mouse and Mechanical Keyboard), demonstrating the many-to-many relationship between `orders` and `products` through the `order_items` association table.


---

## Checkpoint 3 - Full API, Testing & Quality Assurance

### Overview

RevoShop is a backend system for an online store. It exposes a REST API built with
Flask and SQLAlchemy on top of a PostgreSQL database, covering user registration and
login, product and category management, and order placement with a many-to-many
relationship between orders and products.

### Live Deployment

The API is deployed and publicly accessible on Render, backed by a hosted PostgreSQL
database on Supabase:

**Base URL:** <https://revoshop-sgjp.onrender.com>

The Flask backend runs under Gunicorn on Render, with all migrations applied to the
Supabase database via `flask db upgrade`. Sensitive configuration (`DATABASE_URL`,
`SECRET_KEY`, `DEBUG`) is provided through Render's environment variables rather than a
committed `.env` file. All CRUD endpoints are reachable at the base URL above — for
example:

- `GET https://revoshop-sgjp.onrender.com/products` — list all products
- `GET https://revoshop-sgjp.onrender.com/products/1` — get a single product
- `GET https://revoshop-sgjp.onrender.com/categories` — list all categories

> Note: On Render's free tier the service sleeps after inactivity, so the first request
> after an idle period may take a few seconds to spin up.

### Features Implemented

- **Full CRUD for Products** — create, list, retrieve, update, and delete, with the
  delete blocked when a product is still linked to active orders (pending, processing,
  or shipped).
- **Full CRUD for Categories** — create, list, retrieve (including the category's
  products), update, and delete.
- **Full CRUD for Orders** — place an order linked to a user, list a user's orders,
  view a single order with its items and product details, update, and delete.
- **User registration and login** — `POST /users` and `POST /auth/login`.
- **Many-to-many relationship** between orders and products through the `order_items`
  association table (with `quantity` and `unit_price` captured at time of purchase).
- **Data validation** on product and category input (required fields, non-negative
  price and stock, valid category reference).
- **Error handling** with `try/except` and `db.session.rollback()`, returning
  meaningful JSON error messages with appropriate HTTP status codes.
- **Deletion guard** preventing removal of a product that still has active orders.

### API Endpoints

| Module     | Method | Endpoint               | Description                                   |
|------------|--------|------------------------|-----------------------------------------------|
| User       | POST   | `/users`               | Register a new user                           |
| Auth       | POST   | `/auth/login`          | Log in                                        |
| Product    | POST   | `/products`            | Create a new product                          |
| Product    | GET    | `/products`            | List all products                             |
| Product    | GET    | `/products/<id>`       | Get a specific product                        |
| Product    | PUT    | `/products/<id>`       | Update a product                              |
| Product    | DELETE | `/products/<id>`       | Delete a product (blocked if active orders)   |
| Category   | POST   | `/categories`          | Create a new category                         |
| Category   | GET    | `/categories`          | List all categories                           |
| Category   | GET    | `/categories/<id>`     | Get a category with its products              |
| Category   | PUT    | `/categories/<id>`     | Update a category                             |
| Category   | DELETE | `/categories/<id>`     | Delete a category                             |
| Order      | POST   | `/orders`              | Place a new order (send `user_id` in body)    |
| Order      | GET    | `/orders?user_id=<id>` | List all orders for a user                    |
| Order      | GET    | `/orders/<id>`         | View an order with items and product details  |
| Order      | PUT    | `/orders/<id>`         | Update an order (e.g. status)                 |
| Order      | DELETE | `/orders/<id>`         | Delete an order                               |

### Technologies Used

- Flask
- SQLAlchemy
- Flask-Migrate
- PostgreSQL (hosted on Supabase)
- pgAdmin / DBeaver
- pytest
- Locust
- python-dotenv
- gunicorn (production WSGI server)
- Render (deployment platform)

### Environment Variables

Sensitive configuration lives in a `.env` file (never committed) and is read via
`python-dotenv` and `os.getenv()`. A safe-to-commit `.env.example` provides
placeholders:

```text
DATABASE_URL=postgresql://user:password@localhost:5432/revoshop_db
SECRET_KEY=your-secret-key-here
DEBUG=True
```

Copy it to `.env` and fill in your real values:

```bash
cp .env.example .env
```

### How to Run Locally

```bash
# 1. Clone the repo
git clone <repo-url>
cd module-2-muhihsann

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment variables and fill in your DB password
cp .env.example .env

# 5. Apply migrations (creates all tables incl. the role column)
flask db upgrade

# 6. (Optional) Seed sample data
psql -U postgres -d revoshop_db -f database/seed.sql

# 7. Run the app
python run.py
```

### Running the Tests

Category CRUD is covered by pytest, testing both happy-path and error cases:

```bash
pytest tests/test_categories.py -v
```

### Running the Load Test (Locust)

With the Flask server running on port 5000, start Locust in another terminal:

```bash
locust -f locustfile.py --host http://127.0.0.1:5000
```

Open <http://localhost:8089>, set the number of users (tested from 50 up to 200 with a
spawn rate of 10) and start the simulation. The load test runs a sequential user
journey: list products, get a single product, place an order, then fetch the created
order.

---

## Checkpoint 3 - Image Evidence

Check out the `img/` folder for the full evidence:

- `img/postman/CRUD/` — Postman requests for the full CRUD cycle (POST, GET, PUT,
  DELETE) plus login and error cases (400 / 404 / 409).
- `img/pytest/` — pytest run showing all Category CRUD tests passing.
- `img/locust/` — Locust dashboards and charts for 50, 100, 150, and 200 users.
- `img/added_users5_role.png` — the `role` column added to `users`.
- `img/many_to_many.png` — the `order_items` association table linking one order to
  multiple products.

**Product CRUD cycle (Postman)**

Create → Fetch → Update → Delete:

![POST new product](img/postman/CRUD/POST_newproducts.png)
![GET new product](img/postman/CRUD/GET_newproducts9.png)
![PUT product](img/postman/CRUD/PUT_products9.png)
![DELETE product](img/postman/CRUD/DEL_products9.png)

**Validation and error cases (Postman)**

![POST 409 already exists](img/postman/CRUD/POST_409alreadyexists.png)
![PUT 400 bad request](img/postman/CRUD/PUT_400badrequest.png)
![GET 404 not found](img/postman/CRUD/GET_products99_404.png)
![DELETE 404 not found](img/postman/CRUD/DEL_products10_404.png)

**Login (Postman)**

![Auth login](img/postman/CRUD/Auth%20Login%20User5.png)

**pytest — Category CRUD tests passing**

![pytest results](img/pytest/pytest.png)

**Locust — load test (50 to 200 users)**

![Locust 50 users](img/locust/Locust_50U_10Rate.png)
![Locust 100 users](img/locust/Locust_100U_10Rate.png)
![Locust 150 users](img/locust/Locust_150U_10Rate.png)
![Locust 200 users](img/locust/Locust_200U_10Rate.png)

**Locust — charts (50 to 200 users)**

![Locust chart 50 users](img/locust/LocustChart_50U_10Rate.png)
![Locust chart 100 users](img/locust/LocustChart_100U_10Rate.png)
![Locust chart 150 users](img/locust/LocustChart_150U_10Rate.png)
![Locust chart 200 users](img/locust/LocustChart_200U_10Rate.png)

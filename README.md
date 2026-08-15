# RevoShop Database

Backend database schema for RevoShop, an online store. Built with PostgreSQL.


## Entities
Check out `revoshop_db.png` for the detailed server tree.
Link : https://github.com/Revou-FSSE-Jun26/module-2-muhihsann/blob/54a5868bddba67a29c1ee4a80558565a91f1e589/img/revoshop_db.png
![Alt_Text](https://github.com/Revou-FSSE-Jun26/module-2-muhihsann/blob/54a5868bddba67a29c1ee4a80558565a91f1e589/img/revoshop_db.png)
- **users** — customer accounts
- **categories** — product categories
- **products** — store items, each linked to a category
- **orders** — placed by a user
- **order_items** — junction table linking orders and products

Check out `erd.png` for the full schema diagram.
Link : https://github.com/Revou-FSSE-Jun26/module-2-muhihsann/blob/54a5868bddba67a29c1ee4a80558565a91f1e589/img/erd.png
![Alt_Text](https://github.com/Revou-FSSE-Jun26/module-2-muhihsann/blob/54a5868bddba67a29c1ee4a80558565a91f1e589/img/erd.png)


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

Check out `img/postman` for the demo!
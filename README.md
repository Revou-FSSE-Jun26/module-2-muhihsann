# RevoShop Database

Backend database schema for RevoShop, an online store. Built with PostgreSQL.


## Entities

- **users** — customer accounts
- **categories** — product categories
- **products** — store items, each linked to a category
- **orders** — placed by a user
- **order_items** — junction table linking orders and products

See `erd.png` for the full schema diagram.


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


## Notes

- The `users` table intentionally has **no `role` column** at this stage since it will be use via a schema migration in the next checkpoint.
- All primary keys are named `id` and use `SERIAL` for auto-increment.


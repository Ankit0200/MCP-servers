DB_FILE = "my_app.db"
import sqlite3
import random

def setup_dummy_db(total_users: int = 50, total_orders: int = 50):
    """Create tables and ensure there are up to `total_users` users and
    `total_orders` orders in the database. Preserves existing rows and
    only inserts missing rows to reach the target counts.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 1. Create Tables
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS orders (order_id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL)"
    )

    # 2. Ensure some base users exist (preserve prior examples if DB empty)
    cursor.execute("SELECT count(*) FROM users")
    user_count = cursor.fetchone()[0]
    if user_count == 0:
        print("Initializing database with example users...")
        seed_users = [
            (1, "Ankit Devkota", "ankit.intern200@gmail.com"),
            (2, "Alice Smith", "alice@example.com"),
            (3, "Bob Jones", "bob@example.com"),
        ]
        cursor.executemany(
            "INSERT INTO users (id, name, email) VALUES (?, ?, ?)", seed_users
        )
        conn.commit()
        user_count = 3

    # Add additional users up to total_users without duplicating ids
    if user_count < total_users:
        max_id = cursor.execute("SELECT COALESCE(MAX(id), 0) FROM users").fetchone()[0]
        new_users = []
        for i in range(max_id + 1, total_users + 1):
            new_users.append((i, f"User {i}", f"user{i}@example.com"))
        cursor.executemany(
            "INSERT INTO users (id, name, email) VALUES (?, ?, ?)", new_users
        )

    # 3. Ensure orders exist up to total_orders. Assign orders to random existing users.
    cursor.execute("SELECT count(*) FROM orders")
    orders_count = cursor.fetchone()[0]
    if orders_count < total_orders:
        # choose a sensible starting order id based on existing max (or 100 if none)
        max_order_id = cursor.execute("SELECT COALESCE(MAX(order_id), 100) FROM orders").fetchone()[0]
        start_oid = max_order_id + 1 if max_order_id >= 100 else 101
        needed = total_orders - orders_count
        max_user_id = cursor.execute("SELECT COALESCE(MAX(id), 0) FROM users").fetchone()[0]
        new_orders = []
        random.seed(0)  # deterministic amounts and user assignment for repeatability
        for j in range(needed):
            oid = start_oid + j
            # pick an existing user id
            user_id = random.randint(1, max_user_id) if max_user_id > 0 else 1
            # create a varied amount (deterministic formula)
            amount = round(5 + ((oid * 3.1415) % 495.75), 2)
            new_orders.append((oid, user_id, amount))
        cursor.executemany(
            "INSERT INTO orders (order_id, user_id, amount) VALUES (?, ?, ?)", new_orders
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    setup_dummy_db()

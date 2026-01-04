import sqlite3
from datetime import datetime, timedelta
import random

DB_PATH = "demo.db"

CUSTOMERS = [
    ("Alice Chen", "alice@example.com", "Seattle"),
    ("Brian Ortiz", "brian@example.com", "Denver"),
    ("Carla Singh", "carla@example.com", "Austin"),
    ("Dev Patel", "dev@example.com", "New York"),
    ("Ella Gomez", "ella@example.com", "Chicago"),
]

PRODUCTS = [
    ("Wireless Mouse", 29.99),
    ("Mechanical Keyboard", 89.50),
    ("USB-C Hub", 39.00),
    ("4K Monitor", 379.99),
    ("Laptop Stand", 42.00),
]


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            city TEXT NOT NULL
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        );

        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            total REAL NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );

        CREATE TABLE order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            line_total REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
        """
    )


def seed_data(conn: sqlite3.Connection) -> None:
    conn.executemany(
        "INSERT INTO customers(name, email, city) VALUES (?, ?, ?);",
        CUSTOMERS,
    )
    conn.executemany(
        "INSERT INTO products(name, price) VALUES (?, ?);",
        PRODUCTS,
    )

    now = datetime.utcnow()
    orders = []
    order_items = []
    for _ in range(25):
        customer_id = random.randint(1, len(CUSTOMERS))
        created_at = now - timedelta(days=random.randint(0, 120))
        # Pick 1-3 products per order
        product_choices = random.sample(range(1, len(PRODUCTS) + 1), k=random.randint(1, 3))
        running_total = 0.0
        for pid in product_choices:
            qty = random.randint(1, 3)
            price = PRODUCTS[pid - 1][1]
            line_total = round(price * qty, 2)
            running_total += line_total
            order_items.append((pid, qty, line_total))
        orders.append((customer_id, round(running_total, 2), created_at.isoformat()))

    conn.executemany(
        "INSERT INTO orders(customer_id, total, created_at) VALUES (?, ?, ?);",
        orders,
    )

    # back-fill order_items with created order_ids
    cur = conn.execute("SELECT id FROM orders ORDER BY id;")
    order_ids = [row[0] for row in cur.fetchall()]
    idx = 0
    for order_id in order_ids:
        # each order has between 1 and 3 items already queued in order_items list
        for _ in range(1, 4):
            if idx >= len(order_items):
                break
            pid, qty, line_total = order_items[idx]
            idx += 1
            conn.execute(
                "INSERT INTO order_items(order_id, product_id, quantity, line_total) VALUES (?, ?, ?, ?);",
                (order_id, pid, qty, line_total),
            )


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        create_schema(conn)
        seed_data(conn)
        conn.commit()
        print(f"Created {DB_PATH} with sample data.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

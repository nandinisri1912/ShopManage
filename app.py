import os
from dotenv import load_dotenv
from decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "shopping_db"),
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def fetch_all(query, params=()):
    conn = get_db()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def fetch_one(query, params=()):
    conn = get_db()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(query, params)
        return cur.fetchone()
    finally:
        cur.close()
        conn.close()

@app.route("/")
def index():
    try:
        stats = {
            "products": fetch_one("SELECT COUNT(*) AS n FROM products")["n"],
            "customers": fetch_one("SELECT COUNT(*) AS n FROM customers")["n"],
            "orders": fetch_one("SELECT COUNT(*) AS n FROM orders")["n"],
            "revenue": fetch_one("SELECT COALESCE(SUM(total_amount), 0) AS n FROM orders WHERE status <> 'Cancelled'")["n"],
        }
        recent_orders = fetch_all("""
            SELECT o.order_id, o.order_date, o.total_amount, o.status, c.customer_name
            FROM orders o JOIN customers c ON c.customer_id=o.customer_id
            ORDER BY o.order_id DESC LIMIT 5
        """)
        return render_template("index.html", stats=stats, recent_orders=recent_orders)
    except Error as e:
        return render_template("error.html", message=f"Could not connect to the database: {e}")

@app.route("/products")
def products():
    q = request.args.get("q", "").strip()
    rows = fetch_all("""
        SELECT * FROM products
        WHERE product_name LIKE %s OR category LIKE %s
        ORDER BY product_id DESC
    """, (f"%{q}%", f"%{q}%"))
    return render_template("products.html", products=rows, q=q)

@app.route("/products/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("product_name", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        try:
            price = Decimal(request.form.get("price", "0"))
            quantity = int(request.form.get("quantity", "0"))
            if not name or price < 0 or quantity < 0:
                raise ValueError("Enter a name and non-negative price and quantity.")
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""INSERT INTO products (product_name, category, price, quantity, description)
                           VALUES (%s, %s, %s, %s, %s)""",
                        (name, category, price, quantity, description))
            conn.commit()
            cur.close()
            conn.close()
            flash("Product added successfully.", "success")
            return redirect(url_for("products"))
        except (ValueError, Error) as e:
            flash(f"Could not add product: {e}", "error")
    return render_template("product_form.html", product=None, heading="Add product")

@app.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    product = fetch_one("SELECT * FROM products WHERE product_id=%s", (product_id,))
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("products"))
    if request.method == "POST":
        try:
            name = request.form.get("product_name", "").strip()
            category = request.form.get("category", "").strip()
            description = request.form.get("description", "").strip()
            price = Decimal(request.form.get("price", "0"))
            quantity = int(request.form.get("quantity", "0"))
            if not name or price < 0 or quantity < 0:
                raise ValueError("Enter a name and non-negative price and quantity.")
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""UPDATE products SET product_name=%s, category=%s, price=%s,
                           quantity=%s, description=%s WHERE product_id=%s""",
                        (name, category, price, quantity, description, product_id))
            conn.commit()
            cur.close()
            conn.close()
            flash("Product updated successfully.", "success")
            return redirect(url_for("products"))
        except (ValueError, Error) as e:
            flash(f"Could not update product: {e}", "error")
    return render_template("product_form.html", product=product, heading="Edit product")

@app.route("/products/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
        conn.commit()
        cur.close()
        conn.close()
        flash("Product deleted.", "success")
    except Error as e:
        flash(f"Could not delete product. It may already be used in an order. Details: {e}", "error")
    return redirect(url_for("products"))

@app.route("/customers")
def customers():
    rows = fetch_all("SELECT * FROM customers ORDER BY customer_id DESC")
    return render_template("customers.html", customers=rows)

@app.route("/customers/add", methods=["GET", "POST"])
def add_customer():
    if request.method == "POST":
        name = request.form.get("customer_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        try:
            if not name or not email:
                raise ValueError("Customer name and email are required.")
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""INSERT INTO customers (customer_name, email, phone, address)
                           VALUES (%s, %s, %s, %s)""", (name, email, phone, address))
            conn.commit()
            cur.close()
            conn.close()
            flash("Customer added successfully.", "success")
            return redirect(url_for("customers"))
        except (ValueError, Error) as e:
            flash(f"Could not add customer: {e}", "error")
    return render_template("customer_form.html")

@app.route("/customers/<int:customer_id>/delete", methods=["POST"])
def delete_customer(customer_id):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM customers WHERE customer_id=%s", (customer_id,))
        conn.commit()
        cur.close()
        conn.close()
        flash("Customer deleted.", "success")
    except Error as e:
        flash(f"Could not delete customer. This customer may have orders. Details: {e}", "error")
    return redirect(url_for("customers"))

@app.route("/orders")
def orders():
    rows = fetch_all("""
        SELECT o.order_id, o.order_date, o.total_amount, o.status, c.customer_name
        FROM orders o JOIN customers c ON c.customer_id=o.customer_id
        ORDER BY o.order_id DESC
    """)
    return render_template("orders.html", orders=rows)

@app.route("/orders/new", methods=["GET", "POST"])
def new_order():
    customers_list = fetch_all("SELECT customer_id, customer_name, email FROM customers ORDER BY customer_name")
    products_list = fetch_all("SELECT product_id, product_name, price, quantity FROM products WHERE quantity > 0 ORDER BY product_name")
    if request.method == "POST":
        try:
            customer_id = int(request.form.get("customer_id", "0"))
            selected = []
            for p in products_list:
                qty = int(request.form.get(f"qty_{p['product_id']}", "0") or 0)
                if qty > 0:
                    selected.append((p["product_id"], qty))
            if not selected:
                raise ValueError("Choose at least one product quantity.")
            conn = get_db()
            conn.start_transaction()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT customer_id FROM customers WHERE customer_id=%s", (customer_id,))
            if not cur.fetchone():
                raise ValueError("Select a valid customer.")
            total = Decimal("0.00")
            lines = []
            for product_id, qty in selected:
                cur.execute("SELECT product_id, product_name, price, quantity FROM products WHERE product_id=%s FOR UPDATE", (product_id,))
                product = cur.fetchone()
                if not product or qty > product["quantity"]:
                    raise ValueError(f"Insufficient stock for product ID {product_id}.")
                price = Decimal(str(product["price"]))
                line_total = price * qty
                total += line_total
                lines.append((product_id, qty, price, line_total))
            cur2 = conn.cursor()
            cur2.execute("INSERT INTO orders (customer_id, total_amount, status) VALUES (%s, %s, 'Placed')", (customer_id, total))
            order_id = cur2.lastrowid
            for product_id, qty, price, line_total in lines:
                cur2.execute("""INSERT INTO order_items (order_id, product_id, quantity, unit_price, line_total)
                                VALUES (%s, %s, %s, %s, %s)""", (order_id, product_id, qty, price, line_total))
                cur2.execute("UPDATE products SET quantity=quantity-%s WHERE product_id=%s", (qty, product_id))
            conn.commit()
            cur2.close()
            cur.close()
            conn.close()
            flash(f"Order #{order_id} placed successfully.", "success")
            return redirect(url_for("order_detail", order_id=order_id))
        except (ValueError, Error) as e:
            try:
                conn.rollback()
                conn.close()
            except Exception:
                pass
            flash(f"Could not place order: {e}", "error")
    return render_template("order_form.html", customers=customers_list, products=products_list)

@app.route("/orders/<int:order_id>")
def order_detail(order_id):
    order = fetch_one("""
        SELECT o.*, c.customer_name, c.email, c.phone, c.address
        FROM orders o JOIN customers c ON c.customer_id=o.customer_id
        WHERE o.order_id=%s
    """, (order_id,))
    if not order:
        flash("Order not found.", "error")
        return redirect(url_for("orders"))
    items = fetch_all("""
        SELECT oi.*, p.product_name FROM order_items oi
        JOIN products p ON p.product_id=oi.product_id WHERE oi.order_id=%s
    """, (order_id,))
    return render_template("order_detail.html", order=order, items=items)

@app.route("/orders/<int:order_id>/status", methods=["POST"])
def update_order_status(order_id):
    status = request.form.get("status")
    if status not in ("Placed", "Completed", "Cancelled"):
        flash("Invalid order status.", "error")
        return redirect(url_for("order_detail", order_id=order_id))
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status=%s WHERE order_id=%s", (status, order_id))
        conn.commit()
        cur.close()
        conn.close()
        flash("Order status updated.", "success")
    except Error as e:
        flash(f"Could not update status: {e}", "error")
    return redirect(url_for("order_detail", order_id=order_id))


@app.route("/analytics")
def analytics():
    try:
        # Summary cards
        stats = fetch_one("""
            SELECT
                (SELECT COUNT(*) FROM orders) AS total_orders,
                (SELECT COUNT(*) FROM orders
                 WHERE status = 'Completed') AS completed_orders,
                (SELECT COALESCE(SUM(total_amount), 0)
                 FROM orders WHERE status = 'Completed') AS revenue,
                (SELECT COALESCE(SUM(oi.quantity), 0)
                 FROM order_items oi
                 JOIN orders o ON o.order_id = oi.order_id
                 WHERE o.status = 'Completed') AS products_sold
        """)

        stats["revenue"] = float(stats["revenue"])
        stats["products_sold"] = int(stats["products_sold"])

        # Daily revenue for the last 30 days
        daily_rows = fetch_all("""
            SELECT DATE(order_date) AS sale_date,
                   SUM(total_amount) AS revenue
            FROM orders
            WHERE status = 'Completed'
              AND order_date >= DATE_SUB(CURDATE(), INTERVAL 29 DAY)
              AND order_date < DATE_ADD(CURDATE(), INTERVAL 1 DAY)
            GROUP BY DATE(order_date)
            ORDER BY sale_date
        """)

        daily_labels = [
            row["sale_date"].strftime("%d %b")
            for row in daily_rows
        ]
        daily_revenue = [
            float(row["revenue"]) for row in daily_rows
        ]

        # Top 7 products by units sold
        product_rows = fetch_all("""
            SELECT p.product_name,
                   SUM(oi.quantity) AS units_sold
            FROM order_items oi
            JOIN products p ON p.product_id = oi.product_id
            JOIN orders o ON o.order_id = oi.order_id
            WHERE o.status = 'Completed'
            GROUP BY p.product_id, p.product_name
            ORDER BY units_sold DESC
            LIMIT 7
        """)

        product_labels = [
            row["product_name"] for row in product_rows
        ]
        product_quantities = [
            int(row["units_sold"]) for row in product_rows
        ]

        # Order status distribution
        status_rows = fetch_all("""
            SELECT status, COUNT(*) AS total
            FROM orders
            GROUP BY status
        """)

        status_labels = [
            row["status"] for row in status_rows
        ]
        status_counts = [
            int(row["total"]) for row in status_rows
        ]

        return render_template(
            "analytics.html",
            stats=stats,
            daily_labels=daily_labels,
            daily_revenue=daily_revenue,
            product_labels=product_labels,
            product_quantities=product_quantities,
            status_labels=status_labels,
            status_counts=status_counts
        )

    except Error as e:
        return render_template(
            "error.html",
            message=f"Could not load analytics: {e}"
        )


@app.route("/health")
def health():
    try:
        row = fetch_one("SELECT DATABASE() AS db_name")
        return {"status": "ok", "database": row["db_name"]}
    except Error as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)

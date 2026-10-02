from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)

# Demo purpose-এর জন্য secret key
app.secret_key = "demo-secret-key"

# ছোট demo product data
PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Mouse", "price": 1200},
    {"id": 3, "name": "Keyboard", "price": 2500},
]


# =========================
# Health Check
# =========================
@app.route("/health")
def health():
    return {
        "status": "ok",
        "application": "Developer Demo App"
    }


# =========================
# Login Page
# =========================
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Demo login credentials
        if username == "qauser" and password == "123456":
            session["user"] = username
            return redirect(url_for("products"))

        return render_template_string("""
            <h2>Login</h2>

            <p style="color:red;">
                Invalid username or password
            </p>

            <form method="POST">
                <input name="username" placeholder="Username">
                <input name="password" type="password" placeholder="Password">
                <button type="submit">Login</button>
            </form>
        """)

    return render_template_string("""
        <h2>Developer Demo App</h2>

        <form method="POST">
            <input name="username" placeholder="Username">
            <input name="password" type="password" placeholder="Password">

            <button type="submit">Login</button>
        </form>
    """)


# =========================
# Product Page
# =========================
@app.route("/products")
def products():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template_string("""
        <h2>Products</h2>

        <p>Welcome, {{ session["user"] }}</p>

        {% for product in products %}

            <div>
                <b>{{ product["name"] }}</b>

                <span>
                    {{ product["price"] }} BDT
                </span>

                <a href="/cart/add/{{ product['id'] }}">
                    Add to Cart
                </a>
            </div>

            <hr>

        {% endfor %}

        <a href="/cart">View Cart</a>
    """, products=PRODUCTS)


# =========================
# Add Product To Cart
# =========================
@app.route("/cart/add/<int:product_id>")
def add_to_cart(product_id):

    if "user" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", [])

    cart.append(product_id)

    session["cart"] = cart

    return redirect(url_for("products"))


# =========================
# Cart
# =========================
@app.route("/cart")
def cart():

    if "user" not in session:
        return redirect(url_for("login"))

    cart_ids = session.get("cart", [])

    cart_products = [
        product
        for product in PRODUCTS
        if product["id"] in cart_ids
    ]

    total = sum(product["price"] for product in cart_products)

    return render_template_string("""
        <h2>Shopping Cart</h2>

        {% for product in products %}

            <p>
                {{ product["name"] }}
                -
                {{ product["price"] }} BDT
            </p>

        {% endfor %}

        <h3>Total: {{ total }} BDT</h3>

        <a href="/products">Back to Products</a>

    """, products=cart_products, total=total)


# =========================
# Run Application
# =========================
if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, redirect, render_template_string, session

app = Flask(__name__)

# Session secret key
app.secret_key = "qa-learning-secret-key"


# ==========================================
# Default Login Credentials
# ==========================================

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"


# ==========================================
# Product Data
# ==========================================

PRODUCTS = [
    {
        "name": "Laptop",
        "price": "50,000 BDT"
    },
    {
        "name": "Mouse",
        "price": "1,000 BDT"
    },
    {
        "name": "Keyboard",
        "price": "2,000 BDT"
    }
]


# ==========================================
# Home Page
# ==========================================

@app.route("/")
def home():

    if "username" in session:
        return redirect("/products")

    return """
    <h1>QA Demo Store</h1>

    <p>Welcome to the QA Automation Demo Application.</p>

    <a href="/login">Login</a>
    """


# ==========================================
# Login Page
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    # Already logged in
    if "username" in session:
        return redirect("/products")

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Validate credentials
        if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:

            # Create login session
            session["username"] = username

            return redirect("/products")

        # Invalid login
        return render_template_string("""
        <h1>Login</h1>

        <p style="color:red;">
            Invalid username or password
        </p>

        <form method="POST">

            <input
                type="text"
                name="username"
                placeholder="Username"
            >

            <br><br>

            <input
                type="password"
                name="password"
                placeholder="Password"
            >

            <br><br>

            <button type="submit">
                Login
            </button>

        </form>

        <p>
            Default Username: admin
        </p>

        <p>
            Default Password: admin123
        </p>
        """)

    # Login form
    return """
    <h1>Login</h1>

    <form method="POST">

        <input
            type="text"
            name="username"
            placeholder="Username"
        >

        <br><br>

        <input
            type="password"
            name="password"
            placeholder="Password"
        >

        <br><br>

        <button type="submit">
            Login
        </button>

    </form>

    <p>
        Default Username: admin
    </p>

    <p>
        Default Password: admin123
    </p>
    """


# ==========================================
# Products Page
# ==========================================

@app.route("/products")
def products():

    # User must be logged in
    if "username" not in session:
        return redirect("/login")

    return render_template_string("""
    <h1>Products</h1>

    <p>
        Welcome, {{ username }}!
    </p>

    <hr>

    <h2>Available Products</h2>

    <ul>
        {% for product in products %}
        <li>
            <strong>{{ product.name }}</strong>
            - {{ product.price }}
        </li>
        {% endfor %}
    </ul>

    <br>

    <a href="/logout">
        <button>
            Logout
        </button>
    </a>
    """,
    username=session["username"],
    products=PRODUCTS
    )


# ==========================================
# Logout
# ==========================================

@app.route("/logout")
def logout():

    # Remove login session
    session.clear()

    return redirect("/login")


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
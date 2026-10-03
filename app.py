
from flask import Flask, request, redirect, render_template_string, session

app = Flask(__name__)

# Session secret key
app.secret_key = "qa-learning-secret-key"

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"

PRODUCTS = [
    {"name": "Laptop", "price": "50,000 BDT"},
    {"name": "Mouse", "price": "1,000 BDT"},
    {"name": "Keyboard", "price": "2,000 BDT"}
]


@app.route("/")
def home():
    if "username" in session:
        return redirect("/products")

    return """
    <h1>QA Demo Store</h1>
    <p>Welcome to the QA Automation Demo Application.</p>

    <a href="/login">Login</a>
    <br><br>
    <a href="/about">About</a>
    """


@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect("/products")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
            session["username"] = username
            return redirect("/products")

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

            <button type="submit">Login</button>
        </form>

        <p>Default Username: admin</p>
        <p>Default Password: admin123</p>
        """)

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

        <button type="submit">Login</button>
    </form>

    <p>Default Username: admin</p>
    <p>Default Password: admin123</p>

    <br>
    <a href="/about">About</a>
    """


@app.route("/products")
def products():
    if "username" not in session:
        return redirect("/login")

    return render_template_string("""
    <h1>Products</h1>

    <p>Welcome, {{ username }}!</p>

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

    <a href="/about">About</a>
    <br><br>

    <a href="/logout">
        <button>Logout</button>
    </a>
    """,
    username=session["username"],
    products=PRODUCTS
    )


# ==========================================
# About Page
# ==========================================

@app.route("/about")
def about():
    return """
    <h1>About QA Demo Store</h1>

    <p>
        QA Demo Store is a simple web application created
        for learning and practicing software quality assurance
        and CI/CD automation.
    </p>

    <h2>Application Features</h2>

    <ul>
        <li>User Login</li>
        <li>Product Listing</li>
        <li>Logout</li>
        <li>Session-based Authentication</li>
        <li>Automated QA Testing</li>
        <li>CI/CD Pipeline Integration</li>
    </ul>

    <h2>Technology</h2>

    <ul>
        <li>Python</li>
        <li>Flask</li>
        <li>Playwright</li>
        <li>Pytest</li>
        <li>GitHub Actions</li>
        <li>Vercel</li>
    </ul>

    <p>
        This application is intended for QA learning,
        automation practice, and CI/CD demonstration.
    </p>

    <br>

    <a href="/">Home</a>
    <br><br>

    <a href="/login">Login</a>
    """


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )


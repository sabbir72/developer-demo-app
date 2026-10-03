from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# Login credentials
USERNAME = "admin"
PASSWORD = "admin123"


# -------------------------
# Home Page
# -------------------------
@app.route("/")
def home():
    return """
    <h1>Demo Store</h1>

    <a href="/login">Login</a>
    """


# -------------------------
# Login Page
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Check login credentials
        if username == USERNAME and password == PASSWORD:
            return redirect("/products")

        return """
        <h2>Invalid username or password</h2>
        <a href="/login">Try Again</a>
        """

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
    """


# -------------------------
# Products Page
# -------------------------
@app.route("/products")
def products():

    return """
    <h1>Products</h1>

    <ul>
        <li>Laptop</li>
        <li>Mouse</li>
        <li>Keyboard</li>
    </ul>
    """


# -------------------------
# Run Application
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
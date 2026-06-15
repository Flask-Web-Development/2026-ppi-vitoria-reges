from flask import Flask, url_for, render_template, request, redirect, abort, session
from markupsafe import escape

app = Flask(__name__)


app.secret_key = "chave-secreta"



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"



@app.route("/about")
def about():
    return "Página sobre"


@app.route("/user/<name>")
def user(name):
    return f"Olá {escape(name)}"



@app.route("/escape/<name>")
def escape_name(name):
    return f"Olá {escape(name)}"



@app.route("/static-test")
def static_test():
    return url_for("static", filename="style.css")



@app.route("/home")
def home():
    return render_template("index.html", name="Vitória")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return f"Usuário {request.form['username']}"
    return "Envie um POST"



@app.route("/go")
def go():
    return redirect(url_for("hello_world"))


@app.route("/erro")
def erro():
    abort(404)



@app.route("/session")
def index():
    if "username" in session:
        return f"Logged in as {session['username']}"
    return "Você não está logado"


@app.route("/session/login", methods=["GET", "POST"])
def session_login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        return redirect(url_for("index"))

    return """
        <form method="post">
            <input name="username">
            <button type="submit">Login</button>
        </form>
    """


@app.route("/session/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))
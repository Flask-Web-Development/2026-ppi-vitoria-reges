from flask import Flask, url_for, render_template, request
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/about")
def about():
    return "Página sobre"

@app.route("/user/<name>")
def user(name):
    return f"Olá {name}"

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
from flask import Flask

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

    from markupsafe import escape

@app.route("/escape/<name>")
def escape_name(name):
    return f"Olá {escape(name)}"

from flask import url_for

@app.route("/static-test")
def static_test():
    return url_for("static", filename="style.css")
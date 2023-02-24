from flask import render_template
from web import app

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return "INDEX PAGE"
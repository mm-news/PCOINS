from flask import Flask
from web import routes

app = Flask(__name__)

from functions import functions

if __name__ == "__main__":
    app.run()
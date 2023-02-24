from flask import Flask

app = Flask(__name__)

from web.web_functions import routes, functions

if __name__ == "__main__":
    app.run()
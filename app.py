from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Tähän tulee book review app"


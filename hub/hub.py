from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
    # Run a jupyter server on a new port
    return "Hello World!"

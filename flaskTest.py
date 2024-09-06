from flask import Flask

app=Flask(__name__)

@app.route("/")

def hello():
    return "Hell O World"

app.run()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

@app.route("/")
def hello_world():
	return "<p>Hello, world</p>"
	

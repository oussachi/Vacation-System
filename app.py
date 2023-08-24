from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

@app.route("/")
def hello_world():
	return "<p>Hello, world</p>"
	
@app.route('/home')
def home():
	return render_template('/user/profil.html')

@app.route("/nouvelle_demande")
def nouvelle_demande():
	return render_template("/user/nouvelleDemande.html")

if __name__ == '__main__':
	app.run(debug=True)
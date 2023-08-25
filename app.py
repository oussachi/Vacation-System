from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
db = SQLAlchemy()

@app.route("/")
def hello_world():
	return render_template('login.html')
	
@app.route('/home')
def home():
	return render_template('/user/profil.html')

@app.route("/nouvelle_demande")
def nouvelle_demande():
	return render_template("/user/nouvelleDemande.html")

@app.route("/mes_demandes")
def mes_demandes():
	demandes = [{
		"date_debut" : datetime.datetime.now(),
		"date_fin" : datetime.datetime.now(),
		"statut" : "Processing"
	}]
	return render_template("/user/demandes.html", demandes = demandes)
if __name__ == '__main__':
	app.run(debug=True)
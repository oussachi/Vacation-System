from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from Controllers.loginController import *
from Controllers.xmlController import *

app = Flask(__name__)
db = SQLAlchemy()

#Login endpoint
@app.route("/", methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		return loginFunction(request)

# ----------------------------------------- Employee Endpoints ------------------------------ #
@app.route('/employé/home')
def home_user():
	return render_template('/user/profil.html')

@app.route("/employé/nouvelle_demande")
def nouvelle_demande():
	return render_template("/user/nouvelleDemande.html")

@app.route("/employé/mes_demandes")
def mes_demandes():
	demandes = [{
		"date_debut" : datetime.datetime.now(),
		"date_fin" : datetime.datetime.now(),
		"statut" : "Refused"
	}]
	return render_template("/user/demandes.html", demandes = demandes)

@app.route("/employé/demande")
def demande():
	return render_template("/user/demande.html")



# ----------------------------------------- GRH Endpoints ------------------------------ #
@app.route("/GRH/home")
def home_GRH():
	return render_template("/GRH/profil.html")

@app.route("/GRH/demandes")
def liste_demande():
	demandes = [{
		"date_debut" : datetime.datetime.now(),
		"date_fin" : datetime.datetime.now(),
		"statut" : "Processing"
	}, {
		"date_debut" : datetime.datetime.now(),
		"date_fin" : datetime.datetime.now(),
		"statut" : "Processing"
	}]
	return render_template("/GRH/listeDemandes.html", demandes=demandes)

@app.route("/GRH/details_demande")
def details_demande():
	return render_template("/GRH/detailsDemande.html")

@app.route("/GRH/motif_refus")
def motif_refus():
	return render_template("/GRH/motif.html")


# ----------------------------------------- Manager Endpoints ------------------------------ #
@app.route("/manager/home")
def home_manager():
	return render_template('/manager/profil.html')

@app.route("/manager/demandes")
def manager_demandes():
	return render_template('/manager/listeDemandes.html')
# ----------------------------------------- Admin Endpoints ------------------------------ #


if __name__ == '__main__':
	app.run(debug=True)
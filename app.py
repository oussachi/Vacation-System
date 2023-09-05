# ------------------------ IMPORTS ------------------------------------ #

from flask import Flask, render_template, request
import datetime
import os
from Models.models import *
basedir = os.path.abspath(os.path.dirname(__file__))


# ----------------------- CONFIGS -------------------------------------- #

app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

db.init_app(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from Controllers.loginController import *
from Controllers.baseController import *
from Controllers.demandeController import *
from Controllers.GRHController import *


# ------------------------ ENDPOINTS -------------------------------- #


#Sign in endpoint
@app.route("/signin", methods=['GET', 'POST'])
def signin():
	if request.method == 'GET':
		return render_template('signin.html')
	else:
		return sign_in(request)


#Login endpoint
@app.route("/", methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		return loginFunction(request)
	
@app.post("/logout")
def logout():
	return log_out()


# ----------------------------------------- Employee Endpoints ------------------------------ #

@app.route('/employé/home')
def home_user():
	user = get_user()
	return render_template('/user/profil.html', user=user)


@app.route("/employé/nouvelle_demande", methods=["GET", "POST"])
def nouvelle_demande():
	user = get_user()
	if (request.method == 'GET'):
		return render_template("/user/nouvelleDemande.html", user=user)
	else:
		return createDemande(request, user)


@app.route("/employé/mes_demandes")
def mes_demandes():
	return getDemandes()


@app.route("/employé/demande/<int:id>")
def demande(id):
	return getDemande(id)


@app.post("/employé/demande/<int:id>/delete")
def delete_demande(id):
	return deleteDemande(id)


@app.route("/employé/demande/<int:id>/edit", methods=['GET', 'POST'])
def edit_demande(id):
	if (request.method == 'POST'):
		return editDemande(request, id)
	else:
		demande = demandeCongé.query.filter_by(id=id).first()
		user = get_user()
		return render_template("/user/modifierDemande.html", user=user, demande=demande)


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


@app.get("/GRH/demandes_compte")
def demandes_compte():
	return getPendingAccounts()

@app.get("/GRH/demande_compte/<int:id>")
def demande_compte(id):
	return getPendingAccount(id)

@app.post("/GRH/demande_compte/<int:id>/approuver")
def approuver_compte(id):
	return approveAccount(id)



# ----------------------------------------- Manager Endpoints ------------------------------ #


@app.route("/manager/home")
def home_manager():
	return render_template('/manager/profil.html')


@app.route("/manager/demandes")
def manager_demandes():
	demandes = [{
		"date_debut" : datetime.datetime.now(),
		"date_fin" : datetime.datetime.now(),
		"statut" : "Processing"
	}, {
		"date_debut" : datetime.datetime.now(),
		"date_fin" : datetime.datetime.now(),
		"statut" : "Processing"
	}]
	return render_template('/manager/listeDemandes.html', demandes=demandes)

@app.route("/manager/demande")
def manager_demande():
	return render_template("/manager/demande.html")

@app.route("/manager/demande/proposition")
def proposition():
	return render_template("/manager/proposition.html")



# ----------------------------------------- Admin Endpoints ------------------------------ #

# ---------------------------------------------------------------------------------------- #
if __name__ == '__main__':
	app.run(debug=True)
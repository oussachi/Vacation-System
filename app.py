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
from Controllers.employeeController import *
from Controllers.GRHController import *
from Controllers.xlsxController import *
from Controllers.managerController import *
from Controllers.adminController import *


# ------------------------ ENDPOINTS -------------------------------- #


#Sign in endpoint
@app.route("/signin", methods=['GET', 'POST'])
def signin():
	return sign_in(request)


#Login endpoint
@app.route("/", methods=['GET', 'POST'])
def login():
	return loginFunction(request)

#Logout endpoint	
@app.post("/logout")
def logout():
	return log_out()

# ----------------------------------------- Employee Endpoints ------------------------------ #


@app.route('/employé/home')
def home_user():
	return getEmployee()


@app.route("/employé/nouvelle_demande", methods=["GET", "POST"])
def nouvelle_demande():
	return createDemande(request)


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
	return editDemande(request, id)

@app.post("/employé/demande/<int:id>/accepter_proposition")
def accepter_proposition(id):
	return acceptProposition(id)


# ----------------------------------------- GRH Endpoints ------------------------------ #


@app.route("/GRH/home")
def home_GRH():
	return getGRH()

@app.route("/GRH/demandes_congé")
def liste_demande():
	return getPendingDemandes()

@app.route("/GRH/demande_congé/<int:id>")
def details_demande(id):
	return getPendingDemande(id)

@app.route("/GRH/demande_congé/<int:id>/refuser", methods=['GET', 'POST'])
def refuser_demande(id):
	return refuseDemande(request, id)

@app.post("/GRH/demande_congé/<int:id>/approuver")
def approuver_demande(id):
	return acceptDemande(request, id)

@app.route("/GRH/gestion_comptes")
def gestion_comptes():
	return getAccountFunctions()

@app.route("/GRH/creation_compte", methods=['GET', 'POST'])
def creation_compte():
	return createAccount(request)

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
	return getManager()


@app.route("/manager/demandes")
def manager_demandes():
	return getPendingDemandes_Manager()


@app.route("/manager/demande/<int:id>")
def manager_demande(id):
	return getPendingDemande_Manager(id)


@app.route("/manager/demande/<int:id>/proposition", methods=['GET', 'POST'])
def proposition(id):
	return proposerDate(request, id)


@app.post("/manager/demande/<int:id>/approuver")
def approuver_demande_manager(id):
	return acceptDemande_Manager(id)


# ----------------------------------------- Admin Endpoints ------------------------------ #

@app.route("/admin/home")
def get_admin():
	return render_template("/admin/profil.html")


@app.route("/admin/fonctions")
def fonctions():
	return render_template("/admin/fonctions.html")


@app.route("/admin/users")
def get_users():
	return getAllUsers()

# ---------------------------------------------------------------------------------------- #
if __name__ == '__main__':
	app.run(debug=True)
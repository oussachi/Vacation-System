#! env/bin/python3
# ------------------------ IMPORTS ------------------------------------ #

from flask import Flask, render_template, request
import os
from Models.models import *
from middleware import *
basedir = os.path.abspath(os.path.dirname(__file__))


# ----------------------- CONFIGS -------------------------------------- #

app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

db.init_app(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

with app.app_context():
	db.create_all()

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


@app.route('/employé/home', endpoint="home_user")
@login_required
@check_if_employee
def home_user():
	return getEmployee()


@app.route("/employé/nouvelle_demande", methods=["GET", "POST"], endpoint='nouvelle_demande')
@login_required
@check_if_employee
def nouvelle_demande():
	return createDemande(request)


@app.route("/employé/mes_demandes", endpoint='mes_demandes')
@login_required
@check_if_employee
def mes_demandes():
	return getDemandes()


@app.route("/employé/demande/<int:id>", endpoint='demande')
@login_required
@check_if_employee
def demande(id):
	return getDemande(id)


@app.post("/employé/demande/<int:id>/delete", endpoint='delete_demande')
@login_required
@check_if_employee
def delete_demande(id):
	return deleteDemande(id)


@app.route("/employé/demande/<int:id>/edit", methods=['GET', 'POST'], endpoint='edit_demande')
@login_required
@check_if_employee
def edit_demande(id):
	return editDemande(request, id)

@app.post("/employé/demande/<int:id>/accepter_proposition", endpoint='accepter_proposition')
@login_required
@check_if_employee
def accepter_proposition(id):
	return acceptProposition(id)


# ----------------------------------------- GRH Endpoints ------------------------------ #


@app.route("/GRH/home", endpoint='home_GRH')
@check_if_GRH
def home_GRH():
	return getGRH()

@app.route("/GRH/gestion_demandes", endpoint='gestion_demandes')
@check_if_GRH
def gestion_demandes():
	return

@app.route("/GRH/demandes_congé", endpoint="liste_demande")
@check_if_GRH
def liste_demande():
	return getPendingDemandes()


@app.route("/GRH/demande_congé/<int:id>", endpoint="details_demande")
@check_if_GRH
def details_demande(id):
	return getPendingDemande(id)


@app.route("/GRH/demande_congé/<int:id>/refuser", methods=['GET', 'POST'], endpoint='refuser_demande')
@check_if_GRH
def refuser_demande(id):
	return refuseDemande(request, id)


@app.post("/GRH/demande_congé/<int:id>/approuver", endpoint="approuver_demande")
@check_if_GRH
def approuver_demande(id):
	return acceptDemande(request, id)


@app.route("/GRH/gestion_comptes", endpoint="gestion_comptes")
@check_if_GRH
def gestion_comptes():
	return getAccountFunctions()


@app.route("/GRH/creation_compte", methods=['GET', 'POST'], endpoint="creation_compte")
@check_if_GRH
def creation_compte():
	return createAccount(request)


@app.get("/GRH/demandes_compte", endpoint="demandes_compte")
@check_if_GRH
def demandes_compte():
	return getPendingAccounts()


@app.get("/GRH/demande_compte/<int:id>", endpoint="demande_compte")
@check_if_GRH
def demande_compte(id):
	return getPendingAccount(id)


@app.post("/GRH/demande_compte/<int:id>/approuver", endpoint="approuver_compte")
@check_if_GRH
def approuver_compte(id):
	return approveAccount(id)


# ----------------------------------------- Manager Endpoints ------------------------------ #


@app.route("/manager/home", endpoint="home_manager")
@check_if_manager
def home_manager():
	return getManager()


@app.route("/manager/demandes", endpoint='manager_demandes')
@check_if_manager
def manager_demandes():
	return getPendingDemandes_Manager()


@app.route("/manager/demande/<int:id>", endpoint='manager_demande')
@check_if_manager
def manager_demande(id):
	return getPendingDemande_Manager(id)


@app.route("/manager/demande/<int:id>/proposition", methods=['GET', 'POST'], endpoint='proposition')
@check_if_manager
def proposition(id):
	return proposerDate(request, id)


@app.post("/manager/demande/<int:id>/approuver", endpoint='approiver_demande_manager')
@check_if_manager
def approuver_demande_manager(id):
	return acceptDemande_Manager(id)


@app.route("/manager/nouvelle_demande", methods=["GET", "POST"], endpoint='nouvelle_demande_manager')
@check_if_manager
def nouvelle_demande_manager():
	return createDemande_manager(request)

@app.route("/manager/mes_demandes", endpoint='mes_demandes_manager')
@check_if_manager
def mes_demandes_manager():
	return getDemandes_manager()

@app.route("/manager/ma_demande/<int:id>", endpoint='demande_manager')
@check_if_manager
def demande_manager(id):
	return getDemande_manager(id)

@app.post("/manager/ma_demande/<int:id>/delete", endpoint='delete_demande_manager')
@check_if_manager
def delete_demande_manager(id):
	return deleteDemande_manager(id)


@app.route("/manager/ma_demande/<int:id>/edit", methods=['GET', 'POST'], endpoint='edit_demande_manager')
@check_if_manager
def edit_demande_manager(id):
	return editDemande_manager(request, id)

# ----------------------------------------- Admin Endpoints ------------------------------ #

@app.route("/admin/home", endpoint='get_admin')
@check_if_admin
def get_admin():
	return render_template("/admin/profil.html")


@app.route("/admin/fonctions", endpoint='fonctions')
@check_if_admin
def fonctions():
	return getFonctions()

@app.route("/admin/users", endpoint='get_users')
@check_if_admin
def get_users():
	return getAllUsers()

@app.route("/admin/demandes", endpoint='get_demandes')
@check_if_admin
def get_demandes():
	return getPendingDemandes_Admin()

@app.route("/admin/demande/<int:id>", endpoint='get_demande')
@check_if_admin
def get_demande(id):
	return getPendingDemande_Admin(id)

@app.post("/admin/demande/<int:id>/approuver", endpoint='approve_account_admin')
@check_if_admin
def approve_account_admin(id):
	return approveAccount_Admin(id)

@app.route("/admin/all_demandes", endpoint='get_all_demandes')
@check_if_admin
def get_all_demandes():
	return getAllPendingAccountDemandes()

# ---------------------------------------------------------------------------------------- #
if __name__ == '__main__':
	app.run(debug=True)
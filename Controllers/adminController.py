from Models.models import db, demandeCongé, userLoginCredentials
from Controllers.xlsxController import *
from Controllers.baseController import *
from flask import session, redirect, render_template
from sqlalchemy import or_


def getFonctions():
    return render_template("/admin/fonctions.html")


def getAllUsers():
    try:
        users = userLoginCredentials.query.all()
        users_data = []
        for user in users:
            if(user.role == 'Employé'):
                data = getUserByMatricule(user.matricule)
                users_data.append(data)
            elif(user.role == 'GRH'):
                data = getGRHByMatricule(user.matricule)
                users_data.append(data)
            elif(user.role == 'Manager'):
                data = getManagerByMatricule(user.matricule)
                users_data.append(data)
        return render_template("/admin/listUsers.html", users=users_data)
    except Exception as e:
        print(users_data)
        return render_template("/admin/listUsers.html", users=users_data, error=str(e))
    
def getPendingDemandes_Admin():
    try:
        admin = get_user()
        if(admin.role != 'Admin'):
            return render_template("/messagePage.html", title="Accounts List", 
                               message=f"Not an admin",
                               link="/")
        list_ = []
        demandes = userLoginCredentials.query.filter(
            or_(
                userLoginCredentials.role == 'GRH', 
                userLoginCredentials.role == 'Manager'
            ),
            userLoginCredentials.account_confirmed == False
        )
        for demande in demandes:
            list_.append(
                userLoginCredentials.query.filter_by(id=demande.id).first()
            )
        return render_template("/admin/listeDemandes.html", comptes=reversed(list_))
    except Exception as e:
        return render_template("/messagePage.html", title="Accounts List", 
                               message=str(e),
                               link="/admin/home")
    


def getPendingDemande_Admin(id):
    try:
        user_data = userLoginCredentials.query.filter_by(id=id).first()
        if(user_data.role == 'GRH'):
            user = getGRHByMatricule(user_data.matricule)
        else:
            user = getManagerByMatricule(user_data.matricule)
        return render_template("/admin/detailsCompte.html", user=user, role=user_data.role)
    except Exception as e:
        return render_template("/messagePage.html", title="Accounts Request", 
                               message=str(e),
                               link="/admin/home")
    

def getAllPendingAccountDemandes():
    try:
        demandes = userLoginCredentials.query.filter_by(account_confirmed=False).all()
        return render_template("/admin/listeDemandes.html", comptes=demandes)
    except Exception as e:
        return render_template("/messagePage.html", title="Accounts List", 
                               message=str(e),
                               link="/admin/home")
    

def approveAccount_Admin(id):
    try:
        account = userLoginCredentials.query.filter_by(id=id).first()
        account.account_confirmed = True
        db.session.commit()
        return render_template("/messagePage.html", title="Account Approval", 
                               message=f"Account of user {account.matricule} has been approved",
                               link="/admin/home")
    except Exception as e:
        return render_template("/admin/detailsCompte.html", error=str(e))
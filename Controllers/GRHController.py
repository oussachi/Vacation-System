from Models.models import *
from flask import render_template, session, redirect
from Controllers.xlsxController import *
from Controllers.baseController import *

def getPendingAccounts():
    try:
        #accounts = userLoginCredentials.query.filter_by(account_confirmed=False)
        code = get_user().matricule
        accounts = []
        matricules = getEmployeesMatriculesByGRHCode(code)
        temps = userLoginCredentials.query.filter(
            userLoginCredentials.matricule.in_(matricules),
            userLoginCredentials.account_confirmed==False)
        for temp in temps:
            accounts.append(
                userLoginCredentials.query.filter_by(id=temp.id).first()
            )
        return render_template("/GRH/listeComptes.html", comptes=accounts)
    except Exception as e:
        return render_template("/GRH/listeComptes.html", error=str(e))

def getPendingAccount(id):
    try:
        account = userLoginCredentials.query.filter_by(id=id).first()
        return render_template("/GRH/detailsCompte.html", user=account)
    except Exception as e:
        return render_template("/GRH/detailsCompte.html", error=str(e))


def approveAccount(id):
    try:
        account = userLoginCredentials.query.filter_by(id=id).first()
        account.account_confirmed = True
        db.session.commit()
        return render_template("/messagePage.html", title="Account Approval", 
                               message=f"Account of user {account.matricule} has been approved")
    except Exception as e:
        return render_template("/GRH/detailsCompte.html", error=str(e))


def getPendingDemandes():
    try:
        code = get_user().matricule
        demandes = []
        matricules = getEmployeesMatriculesByGRHCode(code)
        #demandes = demandeCongé.query.filter_by(statut="Processing")
        temps = demandeCongé.query.filter(
            demandeCongé.employee_matricule.in_(matricules),
            demandeCongé.statut == 'Accepted By Manager'
        )
        for temp in temps:
            demandes.append(
                demandeCongé.query.filter_by(id=temp.id).first()
            )
        return render_template("/GRH/listeDemandes.html", demandes=reversed(demandes))
    except Exception as e:
        return render_template("/GRH/listeDemandes.html", error=str(e))
    

def getPendingDemande(id):
    try:
        demande = demandeCongé.query.filter_by(id=id).first()
        return render_template("/GRH/detailsDemande.html", demande=demande)
    except Exception as e:
        return render_template("/GRH/detailsDemande.html", error=str(e))


def refuseDemande(request, id):
    try:
        demande = demandeCongé.query.filter_by(id=id).first()
        if(request.method=='POST'):
            motif = request.form['motif']
            demande.statut = 'Refused'
            demande.motif_refus = motif
            db.session.commit()
            return render_template("/messagePage.html", title="Refus de demande", 
                                message=f"Demande d'employé {demande.employee_matricule} a été refusée")
        else:
            return render_template("/GRH/motif.html", demande=demande)
    except Exception as e:
        return render_template("/GRH/detailsDemande.html", demande=demande ,error=str(e))
    

def acceptDemande(request, id):
    try:
        demande = demandeCongé.query.filter_by(id=id).first()
        if(request.method=='POST'):
            demande.statut = 'Accepted'
            db.session.commit()
            return render_template("/messagePage.html", title="Refus de demande", 
                                message=f"Demande d'employé {demande.employee_matricule} a été acceptée")
    except Exception as e:
        return render_template("/GRH/detailsDemande.html", demande=demande ,error=str(e))

    
def getGRH():
    matricule = session['user']
    user = getGRHByMatricule(matricule)
    return render_template("/GRH/profil.html", user=user)


def getAccountFunctions():
    return render_template("/GRH/gestionComptes.html")


def createAccount(request):
    try:
        if(request.method == 'GET'):
            return render_template("/GRH/nouveauCompte.html")
        else:
            matricule = request.form['matricule']
            password = request.form['password']
            role = request.form['role']
            user = userLoginCredentials.query.filter_by(matricule=matricule).first()
            if(user == None and password):
                new_user = userLoginCredentials(
                    matricule = matricule,
                    hashed_password = hash_password(password),
                    role = role,
                    account_confirmed = True
                )
                db.session.add(new_user)
                db.session.commit()

                return render_template("/messagePage.html", title="Création de compte", 
                                    message=f"Le compte d'employé {matricule} a été créé avec le mot de passe {password}")
    except Exception as e:
        return render_template("/GRH/nouveauCompte.html", error=str(e))
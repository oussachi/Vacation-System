from Models.models import *
from flask import render_template, session, redirect

def getPendingAccounts():
    try:
        accounts = userLoginCredentials.query.filter_by(account_confirmed=False)
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
        demandes = demandeCongé.query.filter_by(statut="Processing")
        return render_template("/GRH/listeDemandes.html", demandes=demandes)
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
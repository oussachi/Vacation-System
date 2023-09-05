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
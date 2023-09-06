from Models.models import db, demandeCongé
from Controllers.xlsxController import *
from Controllers.baseController import *
from flask import session, redirect, render_template

def getManager():
    matricule = session['user']
    user = getManagerByMatricule(matricule)
    return render_template("/manager/profil.html", user=user)

def getPendingDemandes_Manager():
    try:
        code = session['user']
        demandes = []
        matricules = getEmployeesMatriculesByManagerCode(code)
        temps = demandeCongé.query.filter(
            demandeCongé.employee_matricule.in_(matricules), 
            demandeCongé.statut == 'Processing'
        )
        for temp in temps:
            demandes.append(
                demandeCongé.query.filter_by(id=temp.id).first()
            )
        return render_template("/manager/listeDemandes.html", demandes=demandes)
    except Exception as e:
        return render_template("/manager/listeDemandes.html", error=str(e))
    
def getPendingDemande_Manager(id):
    try:
        demande = demandeCongé.query.filter_by(id=id).first()
        return render_template("/manager/demande.html", demande=demande)
    except Exception as e:
        return render_template("/manager/demande.html", error=str(e))
    
def acceptDemande_Manager(id):
    try:
        demande = demandeCongé.query.filter_by(id=id).first()
        demande.statut = "Accepted By Manager"
        db.session.commit()
        return render_template("/messagePage.html", title="Demande Acceptée",
                               message=f"La demande de congé d'employé {demande.employee_matricule} a été acceptée",
                               link="/manager/home")
    except Exception as e:
        return render_template("/manager/demande.html", error=str(e))
    
def proposerDate(request, id):
    try:
        demande = demandeCongé.query.filter_by(id=id).first()
        if(request.method == 'POST'):
            nouvelle_date_debut = request.form['debut']
            nouvelle_date_fin = request.form['fin']
            demande.date_debut = nouvelle_date_debut
            demande.date_fin = nouvelle_date_fin
            demande.statut = "Modified By Manager"
            db.session.commit()
            return redirect(f"/manager/demande/{demande.id}")
        else:
            return render_template("/manager/proposition.html", demande=demande)
    except Exception as e:
        return render_template("/manager/demande.html", error=str(e))
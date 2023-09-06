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
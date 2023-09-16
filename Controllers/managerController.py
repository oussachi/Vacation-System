from Models.models import db, demandeCongé
from Controllers.xlsxController import *
from Controllers.baseController import *
from flask import session, redirect, render_template
from sqlalchemy import desc

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
            return redirect(f"/manager/demandes")
        else:
            return render_template("/manager/proposition.html", demande=demande, soldesFunc=getEmployeeSoldes)
    except Exception as e:
        return render_template("/manager/demande.html", error=str(e))
    

def createDemande_manager(request):
    try:
        user = get_user()
        if(request.method == 'POST'):
            user_matricule = session['user']
            date_debut = request.form['debut']
            date_fin = request.form['fin']
            if(not(correctDateOrder(date_debut, date_fin))):
                return render_template("/messagePage.html", title="Demande non valide", 
                                message=f"Mauvais ordre des dates",
                                link="/manager/nouvelle_demande")
            elif(not(correctWithSoldesValue(date_debut, date_fin, user_matricule, 'Manager'))):
                return render_template("/messagePage.html", title="Demande non valide", 
                                message=f"Votre solde n'est pas suffisant",
                                link="/manager/nouvelle_demande")
            new_demande = demandeCongé(
                date_debut = date_debut,
                date_fin = date_fin,
                employee_matricule = user_matricule,
                statut = 'Managerial'
            )

            db.session.add(new_demande)
            db.session.commit()
            return redirect('/manager/mes_demandes')
        else:
            return render_template("/manager/nouvelleDemande.html", user=user)
    except Exception as e:
        return render_template('/manager/nouvelleDemande.html',user=user, error=str(e))
    

def getDemandes_manager():
    try:
        user_matricule = session['user']
        demandes = demandeCongé.query.filter_by(employee_matricule=user_matricule).order_by(desc(demandeCongé.id))
        return render_template('/manager/demandes.html', demandes=demandes)
    except Exception as e:
        return render_template('/manager/demandes.html', error=str(e))


def getDemande_manager(id):
    try:
        demande = demandeCongé.query.filter_by(id=id).first()
        return render_template('/manager/ma_demande.html', demande=demande)
    except Exception as e:
        return render_template('/manager/ma_demande.html', error=str(e))


def deleteDemande_manager(id):
    try:
        demande = demandeCongé.query.filter_by(id=id).first()
        db.session.delete(demande)
        db.session.commit()
        return redirect('/manager/mes_demandes')
    except Exception as e:
        return render_template('/manager/ma_demande.html', error=str(e))
    
def editDemande_manager(request, id):
    try:
        if(request.method == 'POST'):
            demande = demandeCongé.query.filter_by(id=id).first()
            nouvelle_date_debut = request.form['debut']
            nouvelle_date_fin = request.form['fin']
            demande.date_debut = nouvelle_date_debut
            demande.date_fin = nouvelle_date_fin
            db.session.commit()
            return redirect(f'/manager/ma_demande/{demande.id}')
        else:
            demande = demandeCongé.query.filter_by(id=id).first()
            user = get_user()
            return render_template("/manager/modifierDemande.html", user=user, demande=demande)
    except Exception as e:
        return render_template('/user/demande.html', error=str(e))
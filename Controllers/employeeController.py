from Models.models import db, demandeCongé
from Controllers.xlsxController import *
from Controllers.baseController import *
from flask import session, redirect, render_template
from sqlalchemy import desc

def createDemande(request):
    try:
        user = get_user()
        if(request.method == 'POST'):
            user_matricule = session['user']
            date_debut = request.form['debut']
            date_fin = request.form['fin']
            new_demande = demandeCongé(
                date_debut = date_debut,
                date_fin = date_fin,
                employee_matricule = user_matricule,
                statut = 'Processing'
            )

            db.session.add(new_demande)
            db.session.commit()

            return redirect('/employé/mes_demandes')
        else:
            return render_template("/user/nouvelleDemande.html", user=user)
    except Exception as e:
        return render_template('/user/nouvelleDemande.html',user=user, error=str(e))
    

def getDemandes():
    try:
        user_matricule = session['user']
        demandes = demandeCongé.query.filter_by(employee_matricule=user_matricule).order_by(desc(demandeCongé.id))
        return render_template('/user/demandes.html', demandes=demandes)
    except Exception as e:
        return render_template('/user/demandes.html', error=str(e))


def getDemande(id):
    try:
        demande = demandeCongé.query.filter_by(id=id).first()
        return render_template('/user/demande.html', demande=demande)
    except Exception as e:
        return render_template('/user/demande.html', error=str(e))


def deleteDemande(id):
    try:
        demande = demandeCongé.query.filter_by(id=id).first()
        db.session.delete(demande)
        db.session.commit()
        return redirect('/employé/mes_demandes')
    except Exception as e:
        return render_template('/user/demande.html', error=str(e))
    
def editDemande(request, id):
    try:
        if(request.method == 'POST'):
            demande = demandeCongé.query.filter_by(id=id).first()
            nouvelle_date_debut = request.form['debut']
            nouvelle_date_fin = request.form['fin']
            demande.date_debut = nouvelle_date_debut
            demande.date_fin = nouvelle_date_fin
            db.session.commit()
            return redirect(f'/employé/demande/{demande.id}')
        else:
            demande = demandeCongé.query.filter_by(id=id).first()
            user = get_user()
            return render_template("/user/modifierDemande.html", user=user, demande=demande)
    except Exception as e:
        return render_template('/user/demande.html', error=str(e))
    
def getEmployee():
    matricule = session['user']
    user = getUserByMatricule(matricule)
    return render_template("/user/profil.html", user=user)

def acceptProposition(id):
    try:
        demande = demandeCongé.query.filter_by(id=id).first()
        demande.statut = 'Accepted By Manager'
        db.session.commit()
        return redirect("/employé/mes_demandes")
    except Exception as e:
        return render_template("")
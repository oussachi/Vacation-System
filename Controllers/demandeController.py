from Models.models import db, demandeCongé
from flask import session, redirect, render_template

def createDemande(request, user):
    try:
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
    except Exception as e:
        return render_template('/user/nouvelleDemande.html',user=user, error=str(e))
    

def getDemandes():
    try:
        user_matricule = session['user']
        demandes = demandeCongé.query.filter_by(employee_matricule=user_matricule)
        return render_template('/user/demandes.html', demandes=demandes)
    except Exception as e:
        return render_template('/user/demandes.html', error=str(e))
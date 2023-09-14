from flask import render_template, session, redirect
from app import db
from Models.models import userLoginCredentials
from Controllers.baseController import *
    

def sign_in(request):
    try:
        if(request.method == 'POST'):
            matricule = request.form['matricule']
            password = request.form['password']
            role = request.form['role']
            user = userLoginCredentials.query.filter_by(matricule=matricule).first()
            if(user == None and password):
                new_user = userLoginCredentials(
                    matricule = matricule,
                    hashed_password = hash_password(password),
                    role = role,
                    account_confirmed = False
                )
                db.session.add(new_user)
                db.session.commit()

                return render_template("/messagePage.html", title="Sign In", 
                                    message="Your account is awaiting approval",
                                    link="/")
            else:
                return render_template('/signin.html', error='User found with given matricule')
        else:
            return render_template("/signin.html")
    except Exception as e:
        return render_template('/signin.html', error=str(e))
    


def loginFunction(request):
    try:
        if(request.method == 'POST'):
            matricule = request.form['matricule']
            password = request.form['password']
            user = userLoginCredentials.query.filter_by(matricule=matricule).first()
            if(not user.account_confirmed):
                return render_template("/messagePage.html", title="Login", 
                                    message="Your account hasn't been approved yet",
                                    link="/")
            if(user):
                hashed_input_password = hash_password(password)
                if(hashed_input_password == user.hashed_password):
                    session['user'] = user.matricule
                    session.permanent = True
                    role = user.role
                    if(role == 'Admin'):
                        return redirect('/admin/home')
                    if(role == 'Manager'):
                        return redirect('/manager/home')
                    elif(role == 'GRH'):
                        return redirect('/GRH/home')
                    return redirect('/employé/home')
                else:
                    return render_template('login.html', error='Wrong password')
            return render_template('login.html', error='No user found for given matricule')
        else:
            return render_template('login.html')
    except Exception as e:
        return render_template('login.html', error=str(e))
    

def log_out():
    try:
        for key in list(session.keys()):
            session.pop(key)
        return redirect("/")
    except Exception as e:
        return redirect("/")
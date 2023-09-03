from flask import render_template, session, redirect
from Controllers.xmlController import *
from app import db
from Models.models import userLoginCredentials
        
def sign_in(request):
    try:
        matricule = request.form['matricule']
        password = request.form['password']
        user = userLoginCredentials.query.filter_by(matricule=matricule).first()
        if(user == None and password):
            new_user = userLoginCredentials(
                matricule = matricule,
                hashed_password = hash(password)
            )
            print(f'{password} ====> {hash(password)}')
            db.session.add(new_user)
            db.session.commit()

            session['user'] = new_user.matricule
            session.permanent = True
            return redirect('/employé/home')
        else:
            return render_template('/signin.html', error='User found with given matricule')
    except Exception as e:
        return render_template('/signin.html', error=str(e))
    

def loginFunction(request):
    try:
        matricule = request.form['matricule']
        password = request.form['password']
        user = userLoginCredentials.query.filter_by(matricule=matricule).first()
        if(user):
            hashed_input_password = hash(password)
            print(f'Login : {password} =====> {hashed_input_password}')
            print(f'user password =====> {user.hashed_password}')
            if(hashed_input_password == user.hashed_password):  
                return redirect('/employé/home')
            else:
                return render_template('login.html', error='Wrong password')
        return render_template('login.html', error='No user found for given matricule')
    except Exception as e:
        return render_template('login.html', error=str(e))
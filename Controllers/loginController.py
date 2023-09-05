from flask import render_template, session, redirect
from app import db
from Models.models import userLoginCredentials
import hashlib
        

def hash_password(password):
    h = hashlib.sha3_256()
    byte_password = bytes(password, 'ascii')
    h.update(byte_password)
    hashed_password = h.hexdigest()
    return hashed_password


def old_sign_in(request):
    try:
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

            session['user'] = new_user.matricule
            session.permanent = True
            
            if(role == 'Manager'):
                return redirect('/manager/home')
            elif(role == 'GRH'):
                return redirect('/GRH/home')
            return redirect('/employé/home')
        else:
            return render_template('/signin.html', error='User found with given matricule')
    except Exception as e:
        return render_template('/signin.html', error=str(e))
    

def sign_in(request):
    try:
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
            if (role=="GRH"):
                new_user.account_confirmed = True
                session['user'] = new_user.matricule
                session.permanent = True
                db.session.add(new_user)
                db.session.commit()
                return redirect('/GRH/home')
            db.session.add(new_user)
            db.session.commit()

            return render_template("/messagePage.html", title="Sign In", 
                                   message="Your account is awaiting approval")
        else:
            return render_template('/signin.html', error='User found with given matricule')
    except Exception as e:
        return render_template('/signin.html', error=str(e))



def old_loginFunction(request):
    try:
        matricule = request.form['matricule']
        password = request.form['password']
        user = userLoginCredentials.query.filter_by(matricule=matricule).first()
        if(user):
            hashed_input_password = hash_password(password)
            if(hashed_input_password == user.hashed_password):
                session['user'] = user.matricule
                session.permanent = True
                role = user.role
                if(role == 'Manager'):
                    return redirect('/manager/home')
                elif(role == 'GRH'):
                    return redirect('/GRH/home')
                return redirect('/employé/home')
            else:
                return render_template('login.html', error='Wrong password')
        return render_template('login.html', error='No user found for given matricule')
    except Exception as e:
        return render_template('login.html', error=str(e))
    


def loginFunction(request):
    try:
        matricule = request.form['matricule']
        password = request.form['password']
        user = userLoginCredentials.query.filter_by(matricule=matricule).first()
        if(not user.account_confirmed):
            return render_template("/messagePage.html", title="Login", 
                                   message="Your account hasn't been approved yet")
        if(user):
            hashed_input_password = hash_password(password)
            if(hashed_input_password == user.hashed_password):
                session['user'] = user.matricule
                session.permanent = True
                role = user.role
                if(role == 'Manager'):
                    return redirect('/manager/home')
                elif(role == 'GRH'):
                    return redirect('/GRH/home')
                return redirect('/employé/home')
            else:
                return render_template('login.html', error='Wrong password')
        return render_template('login.html', error='No user found for given matricule')
    except Exception as e:
        return render_template('login.html', error=str(e))
    
def log_out():
    try:
        for key in list(session.keys()):
            session.pop(key)
        return redirect("/")
    except Exception as e:
        return redirect("/")
from functools import wraps
from flask import session, redirect
from Models.models import *

def login_required(f):
    wraps(f)
    def check_login(*args, **kwargs):
        try:
            session['user']
        except:
            return redirect("/")
        return f(*args, **kwargs)
    return check_login


def check_if_employee(f):
    wraps(f)
    def check_employee(*args, **kwargs):
        try:
            matricule = session['user']
            user = userLoginCredentials.query.filter_by(matricule=matricule).first()
            if (user.role != 'Employé'):
                if(user.role == 'GRH'):
                    return redirect("/GRH/home")
                return redirect("/manager/home")
        except:
            return redirect("/")
        return f(*args, **kwargs)
    return check_employee


def check_if_GRH(f):
    wraps(f)
    def check_GRH(*args, **kwargs):
        try:
            matricule = session['user']
            user = userLoginCredentials.query.filter_by(matricule=matricule).first()
            if (user.role != 'GRH'):
                if(user.role == 'Employé'):
                    return redirect("/Employé/home")
                return redirect("/manager/home")
        except:
            return redirect("/")
        return f(*args, **kwargs)
    return check_GRH


def check_if_manager(f):
    wraps(f)
    def check_manager(*args, **kwargs):
        try:
            matricule = session['user']
            user = userLoginCredentials.query.filter_by(matricule=matricule).first()
            if (user.role != 'Manager'):
                if(user.role == 'GRH'):
                    return redirect("/GRH/home")
                return redirect("/Employé/home")
        except:
            return redirect("/")
        return f(*args, **kwargs)
    return check_manager
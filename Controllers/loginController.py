from Controllers.xmlController import *
from flask import render_template

def find_role(email):
    employees = getElementsByTag('file.xml', 'employe')
    for employee in employees:
        if employee.getElementsByTagName('email')[0].childNodes[0].data == email:
            return 'Employé'
    GRH = getElementsByTag('file.xml', 'GRH')
    for RH in GRH:
        if RH.getElementsByTagName('email')[0].childNodes[0].data == email:
            return 'GRH'
    managers = getElementsByTag('file.xml', 'manager')
    for manager in managers:
        if manager.getElementsByTagName('email')[0].childNodes[0].data == email:
            return 'Manager'
    return 'Admin'


def loginFunction(request):
    email = request.form['email']
    password = request.form['password']
    if(password==""):
        role = find_role(email)
        if(role=='Employé'):
            return render_template('/user/profil.html')
        else:
            return render_template('/GRH/profil.html')
from Models.models import db, demandeCongé, userLoginCredentials
from Controllers.xlsxController import *
from Controllers.baseController import *
from flask import session, redirect, render_template
from sqlalchemy import desc

def getAllUsers():
    try:
        users = userLoginCredentials.query.all()
        users_data = []
        for user in users:
            if(user.role == 'Employé'):
                data = getUserByMatricule(user.matricule)
                users_data.append(data)
            elif(user.role == 'GRH'):
                data = getGRHByMatricule(user.matricule)
                users_data.append(data)
            elif(user.role == 'Manager'):
                data = getManagerByMatricule(user.matricule)
                users_data.append(data)
        return render_template("/admin/listUsers.html", users=users_data)
    except Exception as e:
        print(users_data)
        return render_template("/admin/listUsers.html", users=users_data, error=str(e))
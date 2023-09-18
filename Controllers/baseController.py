from flask import session
from Models.models import *
from Controllers.xlsxController import *
import hashlib
import datetime

def sendResponse(data, message):
    return {
        'result': True,
        'data': data,
        'message': message
    }
    

def sendErrorMessage(message):
    return {
        'result': False,
        'message': message
    }

def get_user():
    user_matricule = session['user']
    user = userLoginCredentials.query.filter_by(matricule=user_matricule).first()
    return user


def hash_password(password):
    h = hashlib.sha3_256()
    byte_password = bytes(password, 'ascii')
    h.update(byte_password)
    hashed_password = h.hexdigest()
    return hashed_password


def correctDateOrder(debut, fin):
    debut = datetime.datetime.strptime(debut, "%Y-%m-%d")
    fin = datetime.datetime.strptime(fin, "%Y-%m-%d")
    diff = fin - debut
    return (diff.days > 0)


def correctWithSoldesValue(debut, fin, matricule, role):
    debut = datetime.datetime.strptime(debut, "%Y-%m-%d")
    fin = datetime.datetime.strptime(fin, "%Y-%m-%d")
    diff = fin - debut
    if(role == 'Employee'):
        soldes = getEmployeeSoldes(matricule)
    else:
        soldes = getManagerSoldes(matricule)
    return (diff.days - 1 <= soldes)
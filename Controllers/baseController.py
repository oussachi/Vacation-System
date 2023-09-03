from flask import session
from Models.models import *

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
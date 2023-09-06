from flask import session
from Models.models import *
import hashlib

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
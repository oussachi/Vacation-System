from flask_sqlalchemy import SQLAlchemy

"""
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prénom = db.Column(db.String(20), unique=False, nullable=False)
    nom = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    telephone = db.Column(db.String, unique=False, nullable=False)
    date_de_naissance = db.Column(db.String, unique=False, nullable=False)
    lieu_de_naissance = db.Column(db.String, unique=False, nullable=False)
    poste = db.Column(db.String, unique=False, nullable=False)
    service = db.Column(db.String, unique=False, nullable=False)
    profil = db.Column(db.String, unique=False, nullable=False)
    congé_acquis_n = db.Column(db.Integer, unique=False, nullable=False)
    congé_acquis_n_1 = db.Column(db.Integer, unique=False, nullable=False)
    requests = db.relationship('VacationRequest', backref='employee')

    def __repr__(self):
        return f'Employee {self.id}: {self.first_name} {self.last_name}'
    
    def toJSON(self):
        return {
                "prénom" : self.prénom,
                "nom" : self.nom,
                "email" : self.email,
                "telephone" : self.telephone,
                "date_de_naissance" : self.date_de_naissance,
                "lieu_de_naissance" : self.lieu_de_naissance,
                "poste" : self.poste,
                "service" : self.service,
                "profil" : self.profil,
                "congé_acquis_n" : self.congé_acquis_n,
                "congé_acquis_n_1" : self.congé_acquis_n_1
        }


class VacationRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, unique=False, nullable=True)
    employee_id = db.Column(db.Ineteger, db.ForeignKey('employee.id', nullable=False))

    def __repr__(self):
        return f'Request {self.id} done by Employee {self.employee_id}'

    def toJSON(self):
        return {
            'id': self.id,
            'content': self.content,
        }
    

class HR(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    telephone = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return f'HR Employee {self.id}: {self.first_name} {self.last_name}'
    
    def toJSON(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'telephone': self.telephone
        }
"""

db = SQLAlchemy()

class userLoginCredentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String, unique=True, nullable=False)
    hashed_password = db.Column(db.String, unique=False, nullable=False)
    role = db.Column(db.String, unique=False, nullable=False)
    account_confirmed = db.Column(db.Boolean, unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.matricule} || Role {self.role}>'
    
    def toJSON(self):
        return {
            'id' : self.id,
            'matricule' : self.matricule,
            'hashed_password' : self.hashed_password
        }
    
class demandeCongé(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_debut = db.Column(db.String, unique=False, nullable=False)
    date_fin = db.Column(db.String, unique=False, nullable=False)
    statut = db.Column(db.String, unique=False, nullable=False)
    employee_matricule = db.Column(db.String, unique=False, nullable=False)
    #employee_matricule = db.Column(db.Ineteger, db.ForeignKey('employee.matricule', nullable=False))

    def __repr__(self):
        return f'Request {self.id} done by Employee {self.employee_matricule}'

    def toJSON(self):
        return {
            'id': self.id,
            'date_debut' : self.date_debut,
            'date_fin' : self.date_fin,
            'employee' : self.employee_matricule
        }
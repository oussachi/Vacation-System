from app import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    telephone = db.Column(db.String, unique=False, nullable=False)
    requests = db.relationship('VacationRequest', backref='employee')

class VacationRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, unique=False, nullable=True)
    employee_id = db.Column(db.Ineteger, db.ForeignKey('employee.id', nullable=False))
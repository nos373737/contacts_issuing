from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return "({0}, {1}, {2})".format(self.id, self.username, self.email)


class SapNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sap_number = db.Column(db.String(8), unique=True, nullable=False)
    contacts = db.relationship("ContactNumber", backref="sap_num")
   

class ContactNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(8), nullable=False)
    sap_num_id = db.Column(db.Integer, db.ForeignKey("sap_number.id"))

    def __repr__(self):
        return "({0})".format(self.description)





    
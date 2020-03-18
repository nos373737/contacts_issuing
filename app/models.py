from . import db
import datetime, enum
from sqlalchemy import Column, Integer, DateTime, Enum
from sqlalchemy.orm import relationship

#Enumeration in Rework
class StatusEnum(enum.Enum):
    ok = "OK"
    nok = "NOK"

class ReturnStatus(enum.Enum):
    new = "NEW"
    recycled = "RECYCLED"

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

    def __repr__(self):
        return "{0}".format(self.sap_number)

class ContactNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(8), nullable=False)
    sap_num_id = db.Column(db.Integer, db.ForeignKey("sap_number.id"))

    def __repr__(self):
        return "{0}".format(self.description)

# class BaysQueue(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     serial_number = db.Column(db.String(20), nullable=False)
#     contact_number = db.Column(db.String(8), nullable=False)
#     return_date = db.Column(DateTime, default=datetime.datetime.now())

#     def __repr__(self):
#         return "({0}, {1}, {2}, {3})".format(self.id, self.serial_number, self.contact_number, self.return_date)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sap_number_id = db.Column(db.Integer, db.ForeignKey("sap_number.id"), nullable = False)
    sap_number = relationship("SapNumber")
    dpn = db.Column(db.String(8), nullable=False)
    serial_number = db.Column(db.String(20), nullable=False)
    create_date = db.Column(DateTime, default=datetime.datetime.now())
    status = db.Column(db.Enum(StatusEnum))

    @classmethod
    def create(cls, **kwargs):
        param = kwargs.items()
        record = cls(sap_number_id=kwargs.get('sap_number'),
            dpn=kwargs.get('dpn'),
            serial_number=kwargs.get('serial_number'),
            create_date=datetime.datetime.now(),
            status=kwargs.get('status'))
        db.session.add(record)
        db.session.commit()


class Return(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(10), nullable=False)
    dpn = db.Column(db.String(8), nullable=False)
    create_date = db.Column(DateTime, default=datetime.datetime.now())
    status = db.Column(db.Enum(ReturnStatus))
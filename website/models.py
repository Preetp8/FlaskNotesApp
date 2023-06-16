from . import db #importing from current (website) package db (db defined as SQLALCEMY in int.py)
from flask_login import UserMixin #custom class to giev user object things specific to it ()
# user mixing for the flask_login module (helps w it)

from sqlalchemy.sql import func # for date time // 

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #makes it so you do not need to specify date (SQLAlchemy does w func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # foreisng key to user 


# whenever you want to make new db model (sotre different type of obj -> dfine the name of object and INHERIT from db.Model)
class User(db.Model, UserMixin):
    # what do you want user to have
    id = db.Column(db.Integer, primary_key = True) #primary key to uniquely iudentify the obj

    email = db.Column(db.String(150), unique=True ) #alwasy have db.Column(then type (string has size arg)) // unique = cant have the same emial as some1 else

    password = db.Column(db.String(150))

    first_name = db.Column(db.String(150))

    # want users to find all of their notes (we will be able to access all the notes user has made thru db.releationship)
    notes = db.relationship('Note') #Flask will add into this User relationship the NOTE id


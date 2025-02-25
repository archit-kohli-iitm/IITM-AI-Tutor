from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.orm import backref

mydb = SQLAlchemy()

class User(mydb.Model):
    uid = mydb.Column(mydb.Integer,primary_key=True,autoincrement=True)
    email = mydb.Column(mydb.Text(100),unique=True,nullable=False)
    active = mydb.Column(mydb.Boolean,default=False)
    password = mydb.Column(mydb.Text(100),nullable=False)
    utype = mydb.Column(mydb.Text(100),nullable=False)
    name = mydb.Column(mydb.Text(100),nullable=False) 
    phone = mydb.Column(mydb.Text(10),nullable=True,server_default='0000000000')
    dob = mydb.Column(mydb.Text(20),nullable=True,server_default='1900-01-01')
    flagged = mydb.Column(mydb.Text(2),nullable=False,server_default='N')
    timestamp = mydb.Column(mydb.DateTime(timezone=True),server_default=func.now())
    chats = mydb.relationship('Chat', backref='user', lazy=True, cascade='all, delete-orphan') # Relationship with Chat model
    def __repr__(self):
        return f'<User {self.uid}>'

class Subject(mydb.Model):
    subject_id = mydb.Column(mydb.Integer, primary_key=True, autoincrement=True)
    name = mydb.Column(mydb.Text(100), nullable=False)
    chats = mydb.relationship('Chat', backref='subject', lazy=True)
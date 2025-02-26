from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.orm import backref

mydb = SQLAlchemy()

class User(mydb.Model):
    uid = mydb.Column(mydb.Integer,primary_key=True,autoincrement=True)
    email = mydb.Column(mydb.Text(100),unique=True,nullable=False)
    active = mydb.Column(mydb.Boolean,default=False)
    password = mydb.Column(mydb.Text(100),nullable=False)
    utype = mydb.Column(mydb.Text(100),nullable=False) # 'tpstudent' or 'tpadmin'
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

class Chat(mydb.Model):
    chat_id = mydb.Column(mydb.Integer, primary_key=True, autoincrement=True)
    uid = mydb.Column(mydb.Integer, mydb.ForeignKey('user.uid'), nullable=False)
    title = mydb.Column(mydb.Text(200), nullable=True, server_default='New Chat')
    subject_id = mydb.Column(mydb.Integer, mydb.ForeignKey('subject.subject_id'), nullable=False)
    created_at = mydb.Column(mydb.DateTime(timezone=True), server_default=func.now())
    messages = mydb.relationship('Message', backref='chat', lazy=True, cascade='all, delete-orphan') # Relationship with Message model

    def __repr__(self):
        return f'<Chat {self.chat_id}>'

class Message(mydb.Model):
    msg_id = mydb.Column(mydb.Integer, primary_key=True, autoincrement=True)
    chat_id = mydb.Column(mydb.Integer, mydb.ForeignKey('chat.chat_id'), nullable=False)
    content = mydb.Column(mydb.Text, nullable=False)
    msg_type = mydb.Column(mydb.Text(50), nullable=False, server_default='user')  # 'user' or 'assistant'
    context = mydb.Column(mydb.Text, nullable=True)
    timestamp = mydb.Column(mydb.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Message {self.msg_id}>'
    
    def to_dict(self):
        return {
            "msg_id": self.msg_id,
            "chat_id": self.chat_id,
            "content": self.content,
            "msg_type": self.msg_type,
            "context": self.context,
            "timestamp": self.timestamp.isoformat()
        }
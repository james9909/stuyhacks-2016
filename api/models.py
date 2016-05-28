from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    uid = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Task(db.Model):
    uid = db.Column(db.Integer,unique=True, primary_key=True)
    priority = db.Column(db.Integer)
    title = db.Column(db.String(20))
    parent = db.Column(db.Integer)
    completed = db.Column(db.Boolean)

    def __init__(self, title, priority = 0, parent = -1, completed = False):
        self.title = title
        self.priority = priority
        self.parent = parent
        self.completed = completed

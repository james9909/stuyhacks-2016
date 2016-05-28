from flask.ext.sqlalchemy import SQLAlchemy

import utils

db = SQLAlchemy()

class User(db.Model):
    uid = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = utils.hash(password)

class Task(db.Model):
    tid = db.Column(db.Integer, unique=True, primary_key=True)
    uid = db.Column(db.Integer)
    priority = db.Column(db.Integer)
    title = db.Column(db.String(20))
    parent = db.Column(db.Integer)
    completed = db.Column(db.Boolean)

    def __init__(self, title, priority = 0, parent = -1, completed = False):
        self.title = title
        self.priority = priority
        self.parent = parent
        self.completed = completed

    def get_children(self):
        children = []
        tasks = Task.query.filter_by(parent=self.tid).all()
        if query is not None:
            for task in tasks:
                children.append({
                    "tid": task.tid,
                    "priority": task.priority,
                    "title": task.title,
                    "parent": task.parent,
                    "completed": task.completed
                })
        return children

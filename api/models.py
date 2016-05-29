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

<<<<<<< HEAD
=======
class Project(db.Model):
    pid = db.Column(db.Integer, unique=True, primary_key=True)
    uid = db.Column(db.Integer)
    title = db.Column(db.String(64))
    tasks = db.relationship("Task", lazy="dynamic")

    def __init__(self, uid, title):
        self.uid = uid
        self.title = title

>>>>>>> 6821b7276d640f22752b477b28a0d24edb413fa7
class Task(db.Model):
    tid = db.Column(db.Integer, unique=True, primary_key=True)
    uid = db.Column(db.Integer)
    priority = db.Column(db.Integer)
    title = db.Column(db.String(64))

    parent = db.Column(db.Integer, db.ForeignKey("task.tid"))
    project = db.Column(db.Integer, db.ForeignKey("project.pid"))
    completed = db.Column(db.Boolean)
    children = db.relationship("Task", uselist=True)

    def __init__(self, uid, title, priority=0, parent=-1, project=-1, completed=False):
        self.uid = uid
        self.title = title
        self.priority = priority
        self.parent = parent
        self.project = project
        self.completed = completed

    def get_children(self):
        tasks = Task.query.filter_by(parent=self.tid).all()
        children = []
        if tasks is not None:
            for task in tasks:
                children.append({
                    "tid": task.tid,
                    "priority": task.priority,
                    "title": task.title,
                    "parent": task.parent,
                    "completed": task.completed,
                    "children": task.children
                })
        return children

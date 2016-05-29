from flask.ext.sqlalchemy import SQLAlchemy

import utils

db = SQLAlchemy()

class User(db.Model):
    uid = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    b_color = db.Column(db.String(32))
    side_color = db.Column(db.String(32))
    nav_color = db.Column(db.String(32))

    def __init__(self, name, email, password, b_color, side_color, nav_color):
        self.name = name
        self.email = email
        self.password = utils.hash(password)
        self.b_color = b_color
        self.side_color = side_color
        self.nav_color = nav_color

#class Project(db.Model):
#    pid = db.Column(db.Integer, unique=True, primary_key=True)
#    #uid
#    title = db.Column(db.String(20))
#
#    def __init__(self, title):
#        self.title = title
#
class Task(db.Model):
    tid = db.Column(db.Integer, unique=True, primary_key=True)
    uid = db.Column(db.Integer)
    priority = db.Column(db.Integer)
    title = db.Column(db.String(20))

    parent = db.Column(db.Integer, db.ForeignKey("task.tid"))
#    project = db.Column(db.Integer)
    completed = db.Column(db.Boolean)
    children = db.relationship("Task", uselist=True)

    def __init__(self, uid, title, priority = 0, parent = -1, completed = False):
        self.uid = uid
        self.title = title
        self.priority = priority
        self.parent = parent
#        self.project = project
        self.completed = completed

#    def update_parents(self):
#        parent = Task.query.filter_by(name=self.parent).first()
#        if ((parent != None) and (not self.parent in task.children)):
#            task.children.append(self.parent)

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

class Project(db.Model):
    pid = db.Column(db.Integer, unique=True, primary_key=True)
    uid = db.Column(db.Integer)
    title = db.Column(db.String(64))
    # tasks = db.relationship("Task", backref="project", lazy="dynamic")
    tasks = []

    def __init__(self, uid, title):
        self.uid = uid
        self.title = title

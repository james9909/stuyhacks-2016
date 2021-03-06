from flask import Flask, redirect, render_template, request, session, url_for

import os

import api

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

with open(".secret_key", "a+b") as f:
    secret_key = f.read()
    if not secret_key:
        secret_key = os.urandom(128)
        f.write(secret_key)
        f.flush()
    app.secret_key = secret_key
    f.close()

with app.app_context():
    from api.models import *
    db.init_app(app)
    db.create_all()

app.register_blueprint(api.projects.blueprint, url_prefix="/api/projects")
app.register_blueprint(api.tasks.blueprint, url_prefix="/api/tasks")
app.register_blueprint(api.users.blueprint, url_prefix="/api/users")

@app.route('/')
def home():
    data = api.users.get_data()
    return render_template("home.html", data=data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route('/register')
def register():
    data = api.users.get_data()
    return render_template("register.html", data=data)

@app.route('/login')
def login():
    data = api.users.get_data()
    return render_template("login.html", data=data)

@app.route("/work")
@api.decorators.redirect_if_not_logged_in("/")
def work():
    data = api.users.get_data()
    taskList = api.tasks.get_task(parent=-1).all()
    projects = api.projects.get_project().all()
    if projects is not None:
        for project in projects:
            tmp = filter(lambda x: x.parent == -1, project.tasks)
            project.tasks = tmp

    return render_template("toDoTemplate.html", data = data, tasks = taskList, projects=projects)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)

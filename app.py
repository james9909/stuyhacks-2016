from flask import Flask, render_template, request, session

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

app.register_blueprint(api.tasks.blueprint, url_prefix="/api/tasks")
app.register_blueprint(api.users.blueprint, url_prefix="/api/users")

@app.route('/')
def home():
    return render_template("home.html", logged_in=False)

@app.route("/logout")
def logout():
    session.clear()
    return render_template("home.html", logged_in=False)

@app.route('/register')
def register():
    return render_template("register.html", logged_in=False)

@app.route('/login')
def login():
    return render_template("login.html", logged_in=False)

@app.route("/work")
def work():
    return render_template("toDoTemplate.html", title= "wtf", logged_in=True)

#@app.route("/test")
#def test():
#    childChild = {"name": "spoopy", "children": []}
#    child1 = {"name": "tomatoC1", "children": []}
#    child2 = {"name": "tomatoC2", "children": [childChild]}
# 
#    tempList = [
#        {
#            "name": "potato 1",
#            "children": [
#                child1,
#                child2
#                ]
#        },
#        {
#            "name": "potato 2",
#            "children": []
#        }
#    ]
#    return render_template("tasks.html", tasks = tempList)
#
#@app.route("/tasks")
#def tasks():
    

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, render_template, request

import api

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

with app.app_context():
    from api.models import *
    db.init_app(app)
    db.create_all()

app.register_blueprint(api.tasks.blueprint, url_prefix="/api/tasks")

@app.route('/')
def home():
    return render_template("home.html", logged_in=False)

@app.route('/register')
def register():
    return render_template("register.html", logged_in=False)

@app.route('/login')
def login():
    return render_template("login.html", logged_in=False)

@app.route("/work")
def work():
    return render_template("toDoTemplate.html", title= "wtf", p = "not like this", logged_in=True)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)

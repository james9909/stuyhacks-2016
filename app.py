from flask import Flask, render_template, request

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

logged_in = False

with app.app_context():
    from api.models import db, User
    db.init_app(app)
    db.create_all()

@app.route('/')
def home():
    return render_template("home.html", logged_in=logged_in)

@app.route('/register')
def register():
    return render_template("register.html", logged_in=logged_in)

@app.route('/login')
def login():
    return render_template("login.html", logged_in=logged_in)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)

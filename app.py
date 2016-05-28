from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

with app.app_context():
    from api.models import db, Users
    db.init_app(app)
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

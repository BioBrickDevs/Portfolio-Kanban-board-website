from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    json,
)
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
import json

app = Flask(__name__)
bootsrap5 = Bootstrap5(app)


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = r"sqlite:///C:\Users\blast\OneDrive\Desktop\Portfolio - 100 days of code\Portfolio - Todo list website\database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Save(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Text, nullable=False)
    value = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/save", methods=["POST"])
def save():
    if request.method == "POST":
        save_data = request.json
        db.session.query(Save).delete()
        db.session.commit()
        for data in save_data["save_data"]:
            new_save = Save(key=data["key"], value=data["value"])
            db.session.add(new_save)
        db.session.commit()
        return "OK"


@app.route("/load", methods=["GET"])
def load():
    if request.method == "GET":
        load_data = Save.query.all()
        data = []
        for load in load_data:
            data.append({"key": load.key, "value": load.value})
        return jsonify({"load_data": data})


app.run(debug=True)

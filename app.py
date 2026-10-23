from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kain-tayo-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(100))
    category = db.Column(db.String(50)) # snacks, lunch, etc.
    status = db.Column(db.String(20), default="Preparing") # Preparing, Ready, Completed
    date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("Login.html")


@app.route("/register")
def register():
    return render_template("Create_account.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/orders")
def orders():
    return render_template("Orders.html")


@app.route("/updates")
def updates():
    return render_template("Updates.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/receipt")
def receipt():
    return render_template("digital_receipt.html")


@app.route("/snacks")
def snacks():
    return render_template("Snacks_menu.html")


@app.route("/lunch")
def lunch():
    return render_template("Lunch_menu.html")


@app.route("/dinner")
def dinner():
    return render_template("Dinner_menu.html")


@app.route("/desserts")
def desserts():
    return render_template("Dessert_menu.html")


@app.route("/beverages")
def beverages():
    return render_template("Beverages_menu.html")


if __name__ == "__main__":
    app.run(debug=True)



from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


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
  

from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("Signup.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/orders")
def orders():
    return render_template("Orders.html")


@app.route("/updates")
def updates():
    return render_template("updates.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/receipt")
def receipt():
    return render_template("digital_receipt.html")


@app.route("/snacks")
def snacks():
    return render_template("snacks_menu.html")


@app.route("/lunch")
def lunch():
    return render_template("lunch_menu.html")


@app.route("/dinner")
def dinner():
    return render_template("dinner_menu.html")


@app.route("/desserts")
def desserts():
    return render_template("dessert_menu.html")


@app.route("/beverages")
def beverages():
    return render_template("beverages_menu.html")


if __name__ == "__main__":
    app.run(debug=True)
  

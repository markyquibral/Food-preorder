from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db'
db = SQLAlchemy(app)

# Database tables
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food = db.Column(db.String(100))
    user_id = db.Column(db.Integer)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for("home"))
        else:
            return "Wrong email or password!"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if User.query.filter_by(email=email).first():
            return "May account na!"
        new_user = User(email=email, password=password)
        db.add(new_user)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("Signup.html")

@app.route("/home")
def home():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    return render_template("home.html")

@app.route("/orders")
def orders():
    all_orders = Order.query.all()
    return render_template("Orders.html", orders=all_orders)

# ... yung ibang menu mo same lang
@app.route("/snacks")
def snacks():
    return render_template("snacks_menu.html")

@app.route("/lunch")
def lunch():
    return render_template("lunch_menu.html")

if __name__ == "__main__":
    app.run(debug=True)

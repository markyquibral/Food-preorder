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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email"), password=request.form.get("password")).first()
        if user:
            session['user_id'] = user.id
            session['email'] = user.email
            return redirect(url_for("home"))
        return "Mali email o password"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if User.query.filter_by(email=request.form.get("email")).first():
            return "May account na!"
        db.session.add(User(email=request.form.get("email"), password=request.form.get("password")))
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("Signup.html")

@app.route("/home")
def home():
    if 'user_id' not in session: return redirect(url_for("login"))
    return render_template("home.html")

# --- DITO YUNG TINATANONG MO ---

@app.route("/orders")
def orders():
    if 'user_id' not in session: return redirect(url_for("login"))
    # Kunin lang order ng naka-login
    my_orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.date.desc()).all()
    return render_template("Orders.html", orders=my_orders)

@app.route("/updates")
def updates():
    if 'user_id' not in session: return redirect(url_for("login"))
    # Dito makikita status kung "Preparing" na o "Ready for pickup"
    my_orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.date.desc()).all()
    return render_template("updates.html", orders=my_orders)

@app.route("/profile")
def profile():
    if 'user_id' not in session: return redirect(url_for("login"))
    user = User.query.get(session['user_id'])
    total_orders = Order.query.filter_by(user_id=session['user_id']).count()
    return render_template("profile.html", user=user, total_orders=total_orders)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Example: pag nag-order sa snacks
@app.route("/order/<category>/<food>")
def make_order(category, food):
    if 'user_id' not in session: return redirect(url_for("login"))
    new_order = Order(food_name=food, category=category, user_id=session['user_id'])
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for("orders"))

if __name__ == "__main__":
    app.run(debug=True)

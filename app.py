from datetime import datetime, timedelta
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "kain_tayo_secret_key_12345"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kain_tayo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# --- Database Models ---
class User(db.Model):
  id = db.Column(db.String(50), primary_key=True)  # Student/Employee ID
  full_name = db.Column(db.String(100), nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  contact = db.Column(db.String(20), nullable=False)


class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_email = db.Column(db.String(100), nullable=False)
  branch = db.Column(db.String(100), nullable=False)
  items_summary = db.Column(db.String(255), nullable=False)
  total = db.Column(db.Float, nullable=False)
  payment_method = db.Column(db.String(50), nullable=False)
  pickup_time = db.Column(db.String(50), nullable=False)
  status = db.Column(db.String(50), default="Pending")
  created_at = db.Column(db.DateTime, default=datetime.utcnow)


# --- Database Initialization & 100 Orders Seeding ---
with app.app_context():
  db.create_all()

  # Create a default user matching your profile UI screenshot if not exists
  if not User.query.filter_by(email="markyquibral").first():
    default_user = User(
        id="CA202403380",
        full_name="markyquibral",
        email="markyquibral",
        password="password123",
        contact="09306612056",
    )
    db.session.add(default_user)
    db.session.commit()

  # Seed 100 orders if the order table is empty
  if Order.query.count() == 0:
    branches = [
        "Cainta Main Branch",
        "Marikina Branch",
        "Pasig Branch",
        "Taytay Branch",
        "Antipolo Branch",
    ]
    sample_items = [
        ("Champorado, Lugaw with Egg", 72.0),
        ("Halo-Halo (Regular) x2", 110.0),
        ("Longsilog", 110.0),
        ("Fried Chicken with Rice, Fruit Salad", 180.0),
        ("Chicken Adobo, Buko Pandan", 130.0),
        ("Tocilog", 110.0),
        ("Pork Sisig with Rice", 70.0),
        ("Beef Bulalo", 90.0),
        ("Pork Sinigang", 70.0),
        ("Lumpia, Turon", 25.0),
    ]
    payment_methods = ["Cash", "GCash", "Maya"]
    statuses = ["Served", "Pending"]

    for i in range(1, 101):
      item_idx = i % len(sample_items)
      branch_idx = i % len(branches)
      pay_idx = i % len(payment_methods)
      status_idx = 0 if i > 5 else 1  # Mostly served, a few pending

      new_order = Order(
          user_email="markyquibral",
          branch=branches[branch_idx],
          items_summary=sample_items[item_idx][0],
          total=sample_items[item_idx][1],
          payment_method=payment_methods[pay_idx],
          pickup_time=f"{(8 + (i % 8)):02d}:00 AM",
          status=statuses[status_idx],
          created_at=datetime.utcnow() - timedelta(days=i % 15),
      )
      db.session.add(new_order)
    db.session.commit()


# --- Authentication & Core Routes ---
@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    data = request.get_json() if request.is_json else request.form
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter(
        (User.email == username) | (User.id == username)
    ).first()
    if user and user.password == password:
      session["user_email"] = user.email
      session["user_name"] = user.full_name
      if request.is_json:
        return jsonify({"success": True}), 200
      return redirect(url_for("home"))

    if request.is_json:
      return jsonify({"message": "Incorrect username or password."}), 401
    return render_template("Login.html")

  return render_template("Login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    data = request.get_json() if request.is_json else request.form
    user_id = data.get("id")
    full_name = data.get("fullName")
    email = data.get("email")
    password = data.get("password")
    contact = data.get("contact")

    if User.query.filter_by(email=email).first():
      if request.is_json:
        return jsonify({"message": "Email already registered."}), 400
      return "Email already registered", 400

    new_user = User(
        id=user_id,
        full_name=full_name,
        email=email,
        password=password,
        contact=contact,
    )
    db.session.add(new_user)
    db.session.commit()

    if request.is_json:
      return jsonify({"success": True}), 200
    return redirect(url_for("login"))

  return render_template("Create_account.html")


# --- Main Application & Menu Routes ---
@app.route("/dashboard")
@app.route("/home")
def home():
  if "user_email" not in session:
    return redirect(url_for("login"))
  return render_template("home.html")


@app.route("/lunch")
def lunch():
  return render_template("Lunch_menu.html")


@app.route("/dinner")
def dinner():
  return render_template("Dinner_menu.html")


@app.route("/snacks")
def snacks():
  return render_template("Snacks_menu.html")


@app.route("/dessert")
def dessert():
  return render_template("Dessert_menu.html")


@app.route("/beverages")
def beverages():
  return render_template("Beverages_menu.html")


@app.route("/orders")
def orders():
  if "user_email" not in session:
    return redirect(url_for("login"))
  user_orders = (
      Order.query.filter_by(user_email=session["user_email"])
      .order_by(Order.created_at.desc())
      .all()
  )
  return render_template("Orders.html", orders=user_orders)


@app.route("/updates")
def updates():
  if "user_email" not in session:
    return redirect(url_for("login"))
  latest_order = (
      Order.query.filter_by(user_email=session["user_email"])
      .order_by(Order.created_at.desc())
      .first()
  )
  return render_template("Updates.html", order=latest_order)


@app.route("/profile")
def profile():
  if "user_email" not in session:
    return redirect(url_for("login"))
  user = User.query.filter_by(email=session["user_email"]).first()
  user_orders = (
      Order.query.filter_by(user_email=session["user_email"])
      .order_by(Order.created_at.desc())
      .all()
  )
  return render_template("profile.html", user=user, orders=user_orders)


@app.route("/receipt")
def receipt():
  return render_template("digital_receipt.html")


# --- API Endpoint to Place Orders ---
@app.route("/api/place-order", methods=["POST"])
def place_order():
  if "user_email" not in session:
    return jsonify({"message": "Unauthorized"}), 401
  data = request.get_json()

  new_order = Order(
      user_email=session["user_email"],
      branch=data.get("branch", "Cainta Main Branch"),
      items_summary=data.get("items_summary", "Champorado, Lugaw with Egg"),
      total=data.get("total", 72.0),
      payment_method=data.get("payment_method", "Cash"),
      pickup_time=data.get("pickup_time", "9:00 AM"),
      status="Pending",
  )
  db.session.add(new_order)
  db.session.commit()
  return jsonify({"success": True, "order_id": new_order.id}), 200


@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for("login"))


if __name__ == "__main__":
  app.run(debug=True)
  

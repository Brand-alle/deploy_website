from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models import show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def index():
    if "log_email" not in session:
        session["log_email"] = ""
    if "first_name" and "last_name" and "email" not in session:
        session["first_name"] = ""
        session["last_name"] = ""
        session["email"] = ""
    return render_template("reg_log.html")

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        session["log_email"] = request.form["log_email"]
    # see if the username provided exists in the database
    valid_user = User.authenticated_user_by_input(request.form)
    if not valid_user:
        return redirect("/")
    session["user_id"] = valid_user.id
    return redirect("/show_wall")

@app.route('/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        session["first_name"] = request.form["first_name"]
        session["last_name"] = request.form["last_name"]
        session["email"] = request.form["email"]
    valid_user = User.create_valid_user(request.form)
    if not valid_user:
        return redirect("/")
    session["user_id"] = valid_user.id
    return redirect("/show_wall")











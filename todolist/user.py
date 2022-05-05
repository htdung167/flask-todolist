from hashlib import sha256
from django.shortcuts import redirect
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

user = Blueprint("user", __name__)


@user.route("/login", methods=["GET", "POST"])
def login():
    from todolist.models import User
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in success!", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Wrong password!", category="error")
        else:
            flash("User doesn't exist!", category="error")
    return render_template("login.html")


@user.route("/signup", methods=["GET", "POST"])
def signup():
    from todolist.models import User, Note
    if request.method == "POST":
        email = request.form.get("email")
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("User existed!", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters!", category="error")
        elif len(password) < 7:
            flash("Password must be greater than 6 characters!", category="error")
        elif password != confirm_password:
            flash("Password doesn't match!", category="error")
        else:
            password = generate_password_hash(password, method="sha256")
            new_user = User(email=email, password=password,
                            user_name=user_name)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("User created!", category="success")
            except:
                flash("User did't create", category="error")

    return render_template("signup.html")


@user.route("/logout")
def logout():
    return "Logout Page"

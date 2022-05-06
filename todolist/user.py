from hashlib import sha256
from django.shortcuts import redirect
from flask import Blueprint, render_template, request, flash, redirect, url_for
from requests import session
from sympy import rem
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db

user = Blueprint("user", __name__)


@user.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Logged in!")
        return redirect(url_for("views.home"))
    from todolist.models import User
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                session.permanent = True 
                login_user(user, remember=True)
                flash("Logged in success!", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Wrong password!", category="error")
        else:
            flash("User doesn't exist!", category="error")
    return render_template("login.html", user=current_user)


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
                login_user(new_user, remember=True)
                session.permanent = True
                return redirect(url_for('views.home'))
            except:
                flash("User did't create!", category="error")

    return render_template("signup.html", user=current_user)


@user.route("/logout")
@login_required # Yeu cau dang nhap truoc 
def logout():
    logout_user()
    return redirect(url_for('user.login'))
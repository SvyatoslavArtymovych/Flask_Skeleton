import uuid
from datetime import datetime

from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from flask import Blueprint, redirect, render_template, url_for, session

from app.models import User
from app.forms import RegisterForm, LoginForm
from app.logger import log

# Set up Bluerints
blueprint = Blueprint("/auth", __name__)


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        user.save()
        log(log.INFO, "Added user [%s]", user)
        return redirect(url_for("/auth.login"))

    return {}
    # return render_template("auth/register.html", form=form)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("/.index"))
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if not check_password_hash(user.password, password):
            error = "Couldn't validate credentials"
            log(log.ERROR, error)
        else:
            login_user(user)
            log(log.INFO, "Login user [%s]", user)
            return redirect(url_for("/.index"))

    return {}
    # return render_template("auth/login.html", form=form, error=error)


@blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for("/auth.login"))
    log(log.INFO, "Logout [%s]", current_user)
    session.clear()
    logout_user()

    return {}
    # return redirect(url_for("/auth.login"))
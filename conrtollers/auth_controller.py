from flask import request, redirect, url_for, flash, render_template
from flask_login import login_user, current_user

from helpers.json import json_response
from models.user import User


def show():
    return render_template('auth/login.html')


def login(req: request):
    email = req.form.get('email')
    password = req.form.get('password')

    if not email or not password:
        return json_response("Empty email or password. Please, try again!", 'error', 404)

    remember = True

    user = User.query.filter_by(email=email).first()

    if user is None or not user or user.password != password:
        flash('Wrong mail or password. Please, try again!')
        return redirect(url_for('route.login'))

    login_user(user, remember=remember)

    return redirect(url_for('route.profile'))


def show_profile():
    if current_user.is_authenticated:
        return render_template('auth/profile.html', email=current_user.email)
    else:
        return redirect(url_for('route.login'))


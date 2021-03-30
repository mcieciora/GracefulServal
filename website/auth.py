from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        pin_code = request.form.get('pin_code')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.pin_code, pin_code):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect pin code, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        pin_code1 = request.form.get('pin_code1')
        pin_code2 = request.form.get('pin_code2')

        user = User.query.filter_by(username=username).first()

        print(pin_code1.isnumeric())

        if user:
            flash('User already exists.', category='error')
        elif pin_code1 != pin_code2:
            flash('Passwords don\'t match.', category='error')
        elif pin_code1.isnumeric() is False or len(pin_code1) != 4:
            flash('Pin code must be 4 digits.', category='error')
        else:
            new_user = User(username=username, pin_code=generate_password_hash(pin_code1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

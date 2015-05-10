from flask import render_template, redirect, url_for, flash
from flask.ext.login import logout_user, login_required, login_user, current_user

from . import auth
from ..models import Agent, TwilioNumber, commit
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Agent.query.filter_by(username=form.username.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, True)
            flash("Logged in successfully.")

            print form.password.data

            user.current_conference = None

            if user.phone is None:
                user.get_new_number()

            if user.phone is None:
                logout_user()
                return render_template('number_error.html')

            return redirect(url_for('main.index'))

        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    number = current_user.phone
    if number is not None:
        twilio_number = TwilioNumber.query.filter_by(number=number).first()
        twilio_number.used = False
        current_user.phone = None
        commit()

    logout_user()
    flash('You have been logged out.')

    return redirect(url_for('main.index'))

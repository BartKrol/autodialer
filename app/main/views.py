from flask import render_template, session, redirect, url_for
from flask.ext.login import current_user, login_required, logout_user
import phonenumbers

from . import main


@main.route('', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated():

        number = current_user.phone

        if number:
            number = phonenumbers.parse(current_user.phone, None)
            number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.NATIONAL)

            return render_template('index.html', known=session.get('known', False), number=number,
                                   clients=current_user.clients)
        else:
            logout_user()
            return redirect(url_for('auth.login'))
    else:
        return redirect('/auth/login')


@login_required
@main.route('clients/', methods=['GET', 'POST'])
def view_clients():
    clients = []
    if current_user.is_authenticated():
        agent = current_user

        clients = agent.clients

    return render_template('clients.html', clients=clients)

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin

from app import db
from . import login_manager


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    surname = db.Column(db.String(60))
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20), unique=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))

    def __repr__(self):
        return '<Client %r>' % self.name


class Agent(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, index=True)
    name = db.Column(db.String(40))
    surname = db.Column(db.String(60))

    phone = db.Column(db.String(20))
    sid = db.Column(db.String(36))

    clients = db.relationship('Client', backref='person',
                              lazy='dynamic')

    conferences = db.relationship('Conference', backref='person',
                                  lazy='dynamic')
    password_hash = db.Column(db.String(128))

    current_conference = db.Column(db.Integer)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_new_number(self):
        number = TwilioNumber.query.filter_by(used=False).first()
        self.phone = number.number
        number.used = True
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return Agent.query.get(int(user_id))


class TwilioNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), unique=True)
    used = db.Column(db.Boolean(), unique=False, default=False)

    def __repr__(self):
        return '<TwilioNumber %r>' % self.number


class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80), unique=True)
    status = db.Column(db.String(20))
    completed = db.Column(db.Boolean(), default=False)
    call = db.Column(db.String(80))
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))


def remove(row):
    db.session.delete(row)
    db.session.commit()


def commit():
    db.session.commit()


def add(element):
    db.session.add(element)
    db.session.commit()

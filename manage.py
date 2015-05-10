#!env/bin/python
import os

from app import create_app, db
from app.models import Agent, Client, TwilioNumber
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Agent=Agent, Client=Client, TwilioNumber=TwilioNumber)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def gunicorn():
    """Run on Heroku"""
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


@manager.command
def populate():
    """Populate with fake data"""
    from fake_data.data import populate

    populate()


@manager.command
def reset():
    """Reset to defaults"""
    numbers = TwilioNumber.query.all()

    for number in numbers:
        number.used = False
        db.session.commit()


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()

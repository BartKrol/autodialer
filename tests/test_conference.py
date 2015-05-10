from unittest import TestCase
from mock import patch

from app import create_app, db, models, conference


def create_database():
    agent = models.Agent(username="Test", name="Bartosz", surname="Krol", password="test")
    number = models.TwilioNumber(number="+441414960198")
    client = models.Client(name="Bartosz", surname="Krol", email="Bartosz.R.Krol@gmail.com", phone="+447700900685")
    agent.clients.append(client)

    models.add(agent)
    models.add(number)

    models.commit()


def conference_status(name, status, return_status):
    conference.views.check_conference_status = lambda x: return_status

    conf = models.Conference(name=name, status=status)

    models.add(conf)


# @patch('conference.views.')
class ConferenceTestCase(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        create_database()

        self.client = self.app.test_client(use_cookies=True)

        self.agent = models.Agent(username="Test", name="Bartosz", surname="Krol", password="test")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_base_status(self):
        conference_status('status-waiting', 'waiting', 'waiting')
        ret = conference.views.control_status(self.agent)

        status = {'status': 'waiting', 'call': 'False'}

        self.assertDictEqual(status, ret)

    def test_status_waiting(self):
        conference_status('status-waiting', 'waiting', 'return-status')

        ret = conference.views.control_status(self.agent)

        status = {'status': 'return-status', 'call': 'False'}

        self.assertDictEqual(status, ret)

    def test_status_completed(self):
        conference_status('status-completed', 'waiting', 'completed')

        ret = conference.views.control_status(self.agent)

        status = {'status': 'completed', 'call': 'False'}

        self.assertDictEqual(status, ret)

        conf_database = models.Conference.query.filter_by(name='status-completed').first()

        self.assertEqual(conf_database.completed, True)






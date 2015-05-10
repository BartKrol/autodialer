from unittest import TestCase
import re

from flask import url_for

from app import create_app, db, models


def create_database():
    agent = models.Agent(username="Test", name="Bruce", surname="Wayne", password="test")
    number = models.TwilioNumber(number="+442079460083")
    client = models.Client(name="Bruce", surname="Banner", email="hulk@smash.com", phone="+441914980954")
    agent.clients.append(client)

    models.add(agent)
    models.add(number)

    models.commit()


class MainTestCase(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        create_database()

        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue("auth/login" in response.headers['location'])

    def test_login(self):
        response = self.client.post(url_for('auth.login'), data={'username': 'Test', 'password': 'test'},
                                    follow_redirects=True)

        data = response.data

        self.assertTrue(re.search('Welcome to Autodialer', data), msg=data)

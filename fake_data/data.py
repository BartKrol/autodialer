from app import models


def populate():
    print "Populating Database with Fake Data"

    agent = models.Agent(username="Test", name="John", surname="Dee", password="test")
    number = models.TwilioNumber(number="+441458570066")

    client = models.Client(name="Tony", surname="Stark", email="i.am@iron.man", phone="+443069990650")
    agent.clients.append(client)

    client = models.Client(name="Bruce", surname="Wayne", email="batman@nanana.com", phone="+443069990884")
    agent.clients.append(client)

    client = models.Client(name="Hermione", surname="Granger", email="hg@hogwarts.com", phone="+443069990642")
    agent.clients.append(client)

    models.add(agent)
    models.add(number)

    models.commit()


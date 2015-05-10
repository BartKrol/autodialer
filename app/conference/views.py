from time import gmtime, strftime

from flask import request, jsonify, url_for, current_app
from twilio.rest import TwilioRestClient
from twilio.twiml import Response
from flask.ext.login import current_user, login_required
import phonenumbers

from . import conference
from .. import models


@conference.route('/', methods=['GET', 'POST'])
def handle_twilio_request():
    """Respond to incoming Twilio requests."""

    now = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    call_number = request.args.get('Called')

    call_number = phonenumbers.parse("+" + call_number, None)
    call_number = phonenumbers.format_number(call_number, phonenumbers.PhoneNumberFormat.E164)

    agent = models.Agent.query.filter_by(phone=call_number).first()

    conference_name = '{time}-{name}'.format(time=now, name=agent.username)

    response = Response()
    with response.dial() as r:
        r.conference(conference_name,
                     beep=False, waitUrl='', startConferenceOnEnter="true",
                     endConferenceOnExit="true")

    conf = models.Conference(name=conference_name, status="waiting", agent_id=agent.id)

    models.add(conf)
    models.commit()

    return str(response)


@conference.route('/status', methods=['GET', 'POST'])
@login_required
def conference_status():
    response = control_status(current_user)
    return jsonify(response)


@conference.route('/call/<client_id>', methods=['GET', 'POST'])
@login_required
def call_to_client(client_id):
    twilio_client = TwilioRestClient(current_app.config['ACCOUNT_SID'], current_app.config['AUTH_TOKEN'])

    client = models.Client.query.get(client_id)
    client_number = client.phone
    conference_id = current_user.current_conference

    call = twilio_client.calls.create(
        url=url_for('.handle_call', conference_id=conference_id, _external=True),
        to=client_number,
        from_=current_user.phone,
        method="GET",
    )

    # Add call sid to conference
    conference = models.Conference.query.get(conference_id)
    conference.call = call.sid
    models.commit()

    return jsonify({'sid': call.sid})


@conference.route('/cancelcall', methods=['GET', 'POST'])
@login_required
def cancel_call():
    twilio_client = TwilioRestClient(current_app.config['ACCOUNT_SID'], current_app.config['AUTH_TOKEN'])

    conference_id = current_user.current_conference
    conf = models.Conference.query.get(conference_id)

    call = twilio_client.calls.update(conf.call, status="completed")

    return jsonify({"sid", call.sid})


@conference.route('/call/handle/<conference_id>', methods=['GET', 'POST'])
def handle_call(conference_id):
    conference = models.Conference.query.get(conference_id)

    response = Response()
    with response.dial() as r:
        r.conference(conference.name,
                     beep=False, waitUrl='', startConferenceOnEnter="true",
                     endConferenceOnExit="false")

    return str(response)


# TODO
@conference.route('/fail', methods=['GET', 'POST'])
def fail():
    print str(request)
    return None


def check_conference_status(conference):
    twilio_client = TwilioRestClient(current_app.config['ACCOUNT_SID'], current_app.config['AUTH_TOKEN'])
    conferences = twilio_client.conferences.list(friendly_name=conference.name)

    if conferences:
        status = str(conferences[0].status)
        conference.status = status
        current_user.current_conference = conference.id
        models.commit()
    else:
        status = conference.status

    return status


def control_status(agent):
    # Check if agent is waiting for conference
    conf = models.Conference.query.filter_by(agent_id=agent.id, status="waiting").first()

    if conf is None:
        conf = models.Conference.query.filter_by(agent_id=agent.id, completed=False).first()

    if conf:
        status = check_conference_status(conf)

        if status == "completed":
            conf.completed = True
            models.commit()

    else:
        status = 'waiting'

    if status == "in-progress":
        call_sid = conf.call

        if call_sid:
            twilio_client = TwilioRestClient(current_app.config['ACCOUNT_SID'], current_app.config['AUTH_TOKEN'])
            call = twilio_client.calls.get(call_sid)
            status = call.status

            return {'status': status, 'call': "True"}

    return {'status': status, 'call': "False"}

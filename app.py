# -*- coding: utf-8 -*-
""" basic routing layer to handle incoming and outgoing requests between our bot and slack """
import json
import jinja2
from flask import render_template, request
from slackeventsapi import SlackEventAdapter
from bot import Bot
from match import generate_matches

matching_bot = Bot()
events_adapter = SlackEventAdapter(matching_bot.verification, "/slack")

template_loader = jinja2.ChoiceLoader([
                    events_adapter.server.jinja_loader,
                    jinja2.FileSystemLoader(['templates']),
                  ])
events_adapter.server.jinja_loader = template_loader


@events_adapter.server.route("/install", methods=["GET"])
def before_install():
    """ renders an installation page for our app """
    client_id = matching_bot.oauth["client_id"]
    return render_template("install.html", client_id=client_id)


@events_adapter.server.route("/thanks", methods=["GET"])
def thanks():
    """ this route renders a page to thank users for installing our app """
    auth_code = request.args.get('code')
    matching_bot.auth(auth_code)
    return render_template("thanks.html")


# here's some helpful debugging hints for checking that env vars are set
@events_adapter.server.before_first_request
def before_first_request():
    client_id = matching_bot.oauth.get("client_id")
    client_secret = matching_bot.oauth.get("client_secret")
    verification = matching_bot.verification
    if not client_id:
        print("Can't find Client ID, did you set this env variable?")
    if not client_secret:
        print("Can't find Client Secret, did you set this env variable?")
    if not verification:
        print("Can't find Verification Token, did you set this env variable?")


@events_adapter.server.route("/slack/generatematches", methods=["POST"])
def handle_generatematches_command():
    """ this route renders a page to thank users for installing our app """
    data = request.data
    # TODO: can i check to see who initiated the slack command from the payload?
    print(data)
    return "OK", 200


# let's add an event handler for messages coming into our bot's test channel
# using the slack events adapter, when we receive a message event
@events_adapter.on("message")
def handle_message(event_data):
    # grab the message from the event payload
    message = event_data["event"]
    # if the user says hello
    if "hello" in message.get('text'):
        # have our bot respond to the message
        matching_bot.say_hello(message)
    else:
        # otherwise help us find out what went wrong
        print("This isn't the message we expected: \n{}\n".format(message))


if __name__ == '__main__':
    events_adapter.start(debug=True)
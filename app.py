# -*- coding: utf-8 -*-
""" basic routing layer to handle incoming and outgoing requests between our bot and slack """
import json
import os

# external package imports
from flask import Flask, render_template, request
import jinja2
from slack import WebClient
from slackeventsapi import SlackEventAdapter

# local project imports 
from src.bot import Bot
from src.store import RaikesMatchBotClient
from src.match import generate_matches

app = Flask(__name__)

# if this becomes more complex, we can use dependency injection
mongo_client = RaikesMatchBotClient()
matching_bot = Bot(mongo_client)
slack_events_adapter = SlackEventAdapter(matching_bot.verification, "/slack")
template_loader = jinja2.ChoiceLoader([
                    slack_events_adapter.server.jinja_loader,
                    jinja2.FileSystemLoader(['templates']),
                  ])
slack_events_adapter.server.jinja_loader = template_loader

@app.route("/install", methods=["GET"])
def before_install():
    """ renders an installation page for our app """
    client_id = matching_bot.oauth["client_id"]
    return render_template("install.html", client_id=client_id)

@app.route("/thanks", methods=["GET"])
def thanks():
    """ this route renders a page to thank users for installing our app """
    auth_code = request.args.get('code')
    matching_bot.auth(auth_code)
    return render_template("thanks.html")

# here's some helpful debugging hints for checking that env vars are set
@app.before_first_request
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

@app.route("/slack/generatematches", methods=["POST"])
def handle_generate_matches_command():
    channel_id = request.form.get('channel_id', None)
    user_id = request.form.get('user_id', None)
    response = ""
    if user_id not in mongo_client.get_admin_users():
        # send unauthorized message
        response = ("Sorry, only specified users are authorized generate matches. "
                    "If you think you should be authorized, reach out to Anna or Mark.")
    else:
        response = matching_bot.generate_matches(channel_id)
    return {
	    "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": response
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Notice an issue or bug? Submit an issue <https://github.com/jShiohaha/slack-matching-bot/issues|here>."
                }
            },
        ],
        "response_type": "in_channel"
    }, 200


if __name__ == '__main__':
    app.run(port=5000)

# -*- coding: utf-8 -*-
import os

# external package imports
from slackclient import SlackClient

class Bot(object):
    def __init__(self):
        super(Bot, self).__init__()
        # when we instantiate a new bot object, we can access the app
        # credentials we set earlier in our local development environment.
        self.oauth = {"client_id": os.environ.get("CLIENT_ID"),
                      "client_secret": os.environ.get("CLIENT_SECRET"),
                      # scopes provide and limit permissions to what our app
                      # can access. it's important to use the most restricted
                      # scope that your app will need.
                      "scope": "bot"}
        self.verification = os.environ.get("VERIFICATION_TOKEN")
        self.client = SlackClient("")

    def auth(self, code):
        """ here we'll create a method to exchange the temporary auth code for an
        oauth token and save it in memory on our bot object for easier access.
        """
        auth_response = self.client.api_call("oauth.access",
                                             client_id=self.oauth['client_id'],
                                             client_secret=self.oauth['client_secret'],
                                             code=code)
        # we'll save the bot_user_id to check incoming messages mentioning our bot
        self.bot_user_id = auth_response["bot"]["bot_user_id"]
        self.client = SlackClient(auth_response["bot"]["bot_access_token"])

    def say_hello(self, message):
        """ here we'll create a method to respond when a user dm's our bot to say hello! """
        channel = message["channel"]
        hello_response = "I want to live! :pray: Please build me <@%s>" % message["user"]
        self.client.api_call("chat.postMessage",
                             channel=channel,
                             text=hello_response)
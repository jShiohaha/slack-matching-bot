# -*- coding: utf-8 -*-
import ast
import json
import os
import requests

# external package imports
from slack import WebClient
from pprint import pprint

# local project imports
from src.match import build_graph, generate_matches, matches_to_str


class Bot(object):
    def __init__(self, store_client):
        super(Bot, self).__init__()
        # when we instantiate a new bot object, we can access the app
        # credentials we set earlier in our local development environment.
        self.oauth = {
            "client_id": os.environ.get("CLIENT_ID"),
            "client_secret": os.environ.get("CLIENT_SECRET"),
            # scopes provide and limit permissions to what our app
            # can access. it's important to use the most restricted
            # scope that your app will need.
            "scope": "bot",
        }
        self.verification = os.environ.get("VERIFICATION_TOKEN")
        self.bot_bearer_token = os.environ.get("BOT_BEARER_TOKEN")
        self.client = WebClient(token=self.bot_bearer_token)
        self.store_client = store_client

    def auth(self, code):
        """ here we'll create a method to exchange the temporary auth code for an
        oauth token and save it in memory on our bot object for easier access.
        """
        auth_response = self.client.api_call(
            "oauth.access",
            client_id=self.oauth["client_id"],
            client_secret=self.oauth["client_secret"],
            code=code,
        )
        # we'll save the bot_user_id to check incoming messages mentioning our bot
        self.bot_user_id = auth_response["bot"]["bot_user_id"]
        self.client = WebClient(token=auth_response["bot"]["bot_access_token"])

    def create_member_ids_to_names_map(self, member_ids):
        members_map = dict()
        member_ids = set(member_ids)  # o(1) lookup when hashed
        for paginated_response in self.client.users_list(limit=200):
            for user in paginated_response["members"]:
                if user["id"] in member_ids:
                    name = user["real_name"]
                    if name is None or name == "":
                        name = user["name"]
                    members_map[user["id"]] = name
        return members_map

    def get_channel_member_ids(self, channel_id):
        def filter_whitelisted_users(user):
            WHITELIST_USERS = self.store_client.get_white_listed_users()
            if user in WHITELIST_USERS:
                return False
            else:
                return True

        response = self.client.conversations_members(channel=channel_id)
        member_ids = response["members"]
        filtered_users = list(filter(filter_whitelisted_users, member_ids))
        return filtered_users

    def format_slack_response(self, message):
        res = {
            "blocks": [
                {"type": "section", "text": {"type": "mrkdwn", "text": message}},
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Notice an issue or bug? Submit an issue <https://github.com/jShiohaha/slack-matching-bot/issues|here>.",
                    },
                },
            ],
        }
        return res

    # TODO: handle any slack / personal exceptions
    def generate_matches(self, channel_id):
        # generate_matches
        member_ids = self.get_channel_member_ids(channel_id)
        graph = self.store_client.get_latest_graph_instance()
        # create graph if None in order to pass by reference
        if graph is None:
            graph = build_graph(member_ids)
        else:
            graph = graph["graph"]
        num_matches, matches = generate_matches(member_ids, graph)
        # avoid extra api calls and computation when there are no matches
        if num_matches <= 0:
            return matches_to_str(num_matches, matches)
        self.store_client.insert_graph_instance(graph)
        members_map = self.create_member_ids_to_names_map(member_ids)
        # convert matches using human readable names from member_map
        matches = [
            [
                members_map[user] if type(match) is list else members_map[match]
                for user in match
            ]
            for match in matches
        ]
        message = self.format_slack_response(matches_to_str(num_matches, matches))
        # send message channel (as bot) with matches
        res = self.client.chat_postMessage(channel=channel_id, blocks=message["blocks"])
        pprint(res)

"""
arc - dead simple chat
Copyright (C) 2017 Jewel Mahanta <jewelmahanta@gmail.com>

This file is part of arc.

arc is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

arc is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with arc.  If not, see <http://www.gnu.org/licenses/>.
"""

from flask import Flask, jsonify, request
from threading import Thread
import websockets
import asyncio
import json
from datetime import datetime
import os
from .auth import Auth
from .database import DB, NoUserError, LengthError, ValidationError


# TODO: Use a message broker (REDIS or rabbitMQ) for sending messages to the
# ws server
class WSClient(Thread):
    def __init__(self):
        Thread.__init__(self, daemon=True)
        self.loop = asyncio.get_event_loop()
        self.ws = None

    def send_message(self, message):
        print(message)
        asyncio.run_coroutine_threadsafe(self.ws.send(message), self.loop)

    async def ws_client(self):
        self.ws = await websockets.connect("ws://ws_server:5555")
        while True:
            greeting = await self.ws.recv()
            # print("< {}".format(greeting))

    # Override :class:`Thread` 's start method and start our
    # websocket thread. We will keep a single thread running
    # for this task.
    def run(self):
        print("Starting ws client thread.")
        self.loop.run_until_complete(self.ws_client())
        self.loop.run_forever()


class APIServer(Flask):
    def __init__(self):
        Flask.__init__(self, __name__)

        # Auth Initialization
        self.auth = Auth(os.environ.get("JWT_SECRET"), "HS256")

        # Database initialization
        self.db = DB()
        self.db.connect()

        # Register the routes
        # TODO: message rate limit 10 per 5 second
        # TODO: message character limit: 2000
        self.route("/api", methods=["GET", "POST"])(self.index)
        self.route("/api/v1/myInfo", methods=["GET"])(self.my_info)
        self.route("/api/v1/messages", methods=["POST"])(self.post_message)
        self.route("/api/v1/auth/login", methods=["POST"])(self.login)
        self.route("/api/v1/auth/register", methods=["POST"])(self.register)

        # start the ws client thread
        self.ws_client = WSClient()
        self.ws_client.start()

    def index(self):
        self.ws_client.send_message("hello there. This is index.")
        return jsonify({
            "hello": "api is working properly"
        }), 200

    # TODO: proper exception handling for this route
    def my_info(self):
        try:
            auth_header = request.headers.get("authorization")
            decoded = self.auth.decode_token(auth_header[7:])
            if decoded:
                user_info = self.db.get_user_info(decoded.get("email"))
                print(user_info)
                return jsonify({
                    "id": user_info[0],
                    "username": user_info[1],
                    "avatar": user_info[2]
                }), 200

            else:
                return jsonify({
                    "error": "Invalid token."
                }), 401

        except KeyError:
            return jsonify({
                "error": "Missing Authorization header."
            }), 400

    def post_message(self):
        try:
            req = request.get_json()
            if req is None:
                return jsonify({
                    "error": "This endpoint only accepts content type application/json."
                }), 400

            content = req.get("content")
            auth_header = request.headers.get("authorization")
            decoded = self.auth.decode_token(auth_header[7:])

            if decoded:
                # TODO: this HAS TO BE CACHED somehow.
                # Hammering the db for every single message won't do.
                user_info = self.db.get_user_info(decoded.get("email"))
                print(user_info)

                self.ws_client.send_message(json.dumps({
                    "type": "POST_MESSAGE",
                    "content": content,
                    "timestamp": datetime.utcnow().isoformat(),
                    "author": {
                        "id": user_info[0],
                        "username": user_info[1],
                        "avatar": user_info[2]
                    }
                }))

                return jsonify({
                    "content": content,
                    "timestamp": datetime.utcnow().isoformat(),
                    "author": {
                        "id": user_info[0],
                        "username": user_info[1],
                        "avatar": user_info[2]
                    }
                }), 200

            else:
                return jsonify({
                    "error": "Invalid token."
                }), 401

        except KeyError:
            return jsonify({
                "error": "message content is not present."
            }), 400

    #  --- Authentication / Registration Routes ---
    def login(self):
        try:
            # print("Request: --> ", request)
            # FIXME: edge case where content-type is application/json but body is blank
            req = request.get_json()
            if req is None:
                return jsonify({
                    "error": "This endpoint only accepts content type application/json."
                }), 400

            email = req["email"]
            password = req["password"]

            # First layer of validation before hitting
            # the database abstraction api.
            if len(email) == 0 or len(password) == 0:
                raise KeyError

            print("Login attempt: {} | {}".format(email, password))
            try:
                if self.db.verify_user(email, password):
                    return jsonify({
                        "token": self.auth.generate_token(email, password)
                    }), 200

                else:
                    return jsonify({
                        "error": "Login failed. Are you sure the password is correct?"
                    }), 401

            except NoUserError as e:
                return jsonify({
                    "error": e.message
                }), 404

        except KeyError:
            return jsonify({
                "error": "Email and password cant be missing or blank."
            }), 400

    def register(self):
        try:
            req = request.get_json()
            if req is None:
                return jsonify({
                    "error": "This endpoint only accepts content type application/json."
                }), 400

            username = req["username"]
            email = req["email"]
            password = req["password"]

            # First layer of validation before hitting
            # the database abstraction api.
            if len(username) == 0 or len(email) == 0 or len(password) == 0:
                raise KeyError

            print("Register attempt: {} | {}".format(email, password))
            try:
                # Returns true if the query executed
                if self.db.create_user(username, email, password):
                    return jsonify({
                        "token": self.auth.generate_token(email, password)
                    }), 200

                # And false if it failed due to integrity error which in
                # our case means this email id already exists.
                else:
                    return jsonify({
                        "error": "This email-id already exists."
                    }), 400

            except ValidationError as e:
                return jsonify({
                    "error": e.message
                }), 400

            except LengthError as e:
                return jsonify({
                    "error": e.message
                }), 400

        except KeyError:
            return jsonify({
                "error": "Username, email and password can't be missing or blank."
            }), 400

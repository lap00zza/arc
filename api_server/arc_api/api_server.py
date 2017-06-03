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


# TODO: Use a message broker (REDIS or rabbitMQ) for sending messages to the WS Server
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


# TODO: Add tests
class APIServer(Flask):
    """
    Represents a arc! Api Server. It is completely stateless and is designed
    to be easily run with gunicorn.
    """
    def __init__(self):
        Flask.__init__(self, __name__)

        # Auth Initialization
        # NOTE: To invalidate all JWT's just change this secret.
        self.auth = Auth(os.environ.get("JWT_SECRET"), "HS256")

        # Database initialization
        self.db = DB()
        self.db.connect()

        # Register the routes
        # TODO: message rate limit 10 per 5 second
        self.route("/api", methods=["GET", "POST"])(self.index)
        self.route("/api/v1/myInfo", methods=["GET"])(self.my_info)
        self.route("/api/v1/messages", methods=["POST"])(self.post_message)
        self.route("/api/v1/auth/login", methods=["POST"])(self.login)
        self.route("/api/v1/auth/register", methods=["POST"])(self.register)

        # start the ws client thread
        self.ws_client = WSClient()
        self.ws_client.start()

    # --- HELPER METHODS ---
    @staticmethod
    def _validate_json_req(req):
        """
        This function makes sure that the request made to the endpoint is of the
        content type application/json. Why? because our full API is JSON only. So
        this acts as the first layer of check.

        Parameters
        ----------
        req: request
            The actual request.
        """
        try:
            json_req = req.get_json()
        except Exception:
            return {
                "error": "This is a very bad request :(. Check the API docs on how to use the arc! api."
            }, 400

        if json_req is None:
            return {
                "error": "This endpoint only accepts content type application/json."
            }, 400

        return json_req, 200

    @staticmethod
    def _validate_type(parsed_req, input_values):
        """
        This function checks the keys in the parsed request and makes sure that they
        are all of :type:`str`. Why str? Coz' why not? Also with string I have to deal
        with less headaches.

        Parameters
        ----------
        parsed_req: Dict
            The parsed request that we got by using request.get_json()
        input_values: list[dict]
            Of the form [{"name": "", "key": ""}]. The name is used while generating
            the error messages. key is well the key in `req` that has to be type checked.
        """
        for item in input_values:
            try:
                if type(parsed_req[item.get("key")]) != str:
                    return {
                        "error": "{} can only be a string.".format(item.get("name"))
                    }, 400

                if len(parsed_req[item.get("key")]) == 0:
                    return {
                        "error": "{} can't be blank.".format(item.get("name"))
                    }, 400

            except KeyError:
                return {
                    "error": "{} is not present.".format(item.get("name"))
                }, 400

        return None, 200

    def _verify(self, req):
        """
        This function makes sure that the Authorization header is present and
        decodes the JWT.

        Parameters
        ----------
        req: request
            The actual request.
        """
        try:
            auth_header = req.headers["authorization"]
        except KeyError:
            return {
                "error": "Missing Authorization header."
            }, 400

        decoded = self.auth.decode_token(auth_header[7:])
        if not decoded:
            return {
                "error": "Invalid token."
            }, 401

        return decoded, 200

    # --- ENDPOINTS START FROM HERE ---
    @staticmethod
    def index():
        return jsonify({
            "hello": "arc! API seems to be working properly."
        }), 200

    # TODO: proper exception handling for this route
    def my_info(self):
        # --- Verify Token ---
        # If there were no errors while decoding the JWT, then
        # data will be the decoded JWT data. If there were error
        # encountered, like missing headers, expired JWT etc. ,
        # then data will the corresponding error message.
        data, code = self._verify(request)
        if code == 200:
            user_info = self.db.get_user_info(data["email"])
            print(user_info)
            return jsonify({
                "id": user_info[0],
                "username": user_info[1],
                "avatar": user_info[2]
            }), code

        else:
            return jsonify(data), code

    def post_message(self):
        # --- Validate JSON ---
        # Note: if the request is valid json then it
        # req will be the parsed JSON. Else req is the
        # error message generated by :meth:_validate_json_req
        req, code = self._validate_json_req(request)
        if code != 200:
            return jsonify(req), code

        #  --- Validate Type ---
        err, code = self._validate_type(req, [{
            "name": "message content",
            "key": "content"
        }])
        if code != 200:
            return jsonify(err), code

        del err

        # --- Limit message size to 2000 characters ---
        if len(req["content"]) > 2000:
            return jsonify({
                "error": "Message content can't be more than 2000 characters."
            }), 400

        #  --- Verify Token ---
        # If there were no errors while decoding the JWT, then
        # data will be the decoded JWT data. If there were error
        # encountered, like missing headers, expired JWT etc. ,
        # then data will the corresponding error message.
        data, code = self._verify(request)
        if code == 200:
            # TODO: this HAS TO BE CACHED somehow.
            # Hammering the db for every single message won't do.
            user_info = self.db.get_user_info(data["email"])
            print(user_info)

            self.ws_client.send_message(json.dumps({
                "type": "POST_MESSAGE",
                "content": req["content"],
                "timestamp": datetime.utcnow().isoformat(),
                "author": {
                    "id": user_info[0],
                    "username": user_info[1],
                    "avatar": user_info[2]
                }
            }))

            return jsonify({
                "content": req["content"],
                "timestamp": datetime.utcnow().isoformat(),
                "author": {
                    "id": user_info[0],
                    "username": user_info[1],
                    "avatar": user_info[2]
                }
            }), code
        else:
            return jsonify(data), code

    #  --- Authentication / Registration Routes ---
    # TODO: tokens should not be handed out so frequently
    def login(self):
        # --- Validate JSON ---
        # Note: if the request is valid json then it
        # req will be the parsed JSON. Else req is the
        # error message generated by :meth:_validate_json_req
        req, code = self._validate_json_req(request)
        if code != 200:
            return jsonify(req), code

        #  --- Validate Type ---
        err, code = self._validate_type(req, [{
            "name": "email",
            "key": "email"
        }, {
            "name": "password",
            "key": "password"
        }])
        if code != 200:
            return jsonify(err), code

        del err

        # --- Code ---
        print("Login attempt: {} | {}".format(req["email"], req["password"]))
        try:
            if self.db.verify_user(req["email"], req["password"]):
                return jsonify({
                    "token": self.auth.generate_token(req["email"], req["password"])
                }), 200

            else:
                return jsonify({
                    "error": "Login failed. Are you sure the password is correct?"
                }), 401

        except ValidationError as e:
            return jsonify({
                "error": e.message
            }), 400

        except LengthError as e:
            return jsonify({
                "error": e.message
            }), 400

        except NoUserError as e:
            return jsonify({
                "error": e.message
            }), 404

    # TODO: tokens should not be handed out so frequently
    def register(self):
        # --- Validate JSON ---
        # Note: if the request is valid json then it
        # req will be the parsed JSON. Else req is the
        # error message generated by :meth:_validate_json_req
        req, code = self._validate_json_req(request)
        if code != 200:
            return jsonify(req), code

        #  --- Validate Type ---
        err, code = self._validate_type(req, [{
            "name": "username",
            "key": "username"
        }, {
            "name": "email",
            "key": "email"
        }, {
            "name": "password",
            "key": "password"
        }])
        if code != 200:
            return jsonify(err), code

        del err

        # --- Code ---
        print("Register attempt: {} | {} | {}".format(req["username"], req["email"], req["password"]))
        try:
            # Returns true if the query executed
            if self.db.create_user(req["username"], req["email"], req["password"]):
                return jsonify({
                    "token": self.auth.generate_token(req["email"], req["password"])
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

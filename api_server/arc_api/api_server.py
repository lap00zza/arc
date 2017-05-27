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

        # Register the routes
        # TODO: message rate limit 10 per 5 second
        # TODO: message character limit: 2000
        self.route("/api", methods=["GET", "POST"])(self.index)
        self.route("/api/messages", methods=["POST"])(self.post_message)

        # start the ws client thread
        self.ws_client = WSClient()
        self.ws_client.start()

    def index(self):
        self.ws_client.send_message("hello there. This is index.")
        return jsonify({
            "hello": "api is working properly"
        })

    def post_message(self):
        try:
            content = request.form["content"]
            author = request.form["author"]
            self.ws_client.send_message(json.dumps({
                "type": "POST_MESSAGE",
                "content": content,
                "author": author
            }))
            return jsonify({
                "success": True
            })

        except KeyError:
            return jsonify({
                "error": "either content or author is not passed"
            })

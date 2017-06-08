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

import asyncio
import websockets
import json
# import datetime
import uuid

__all__ = ["WSServer"]


class WSServer:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.HEART_BEAT_INTERVAL = 30
        self.connected = {}

    @staticmethod
    def generate_event(event_type, data=None, serial=None):
        """
        Generate a event string.

        Parameters
        ----------
        event_type: str
            name of the event
        data: dict
            a dictionary of data to send with this event
        serial: int
            the serial number for the event.

        Returns
        -------
        event: json
            a json formatted event string that can be sent through the websocket
        """
        return json.dumps({
            "type": event_type,
            "data": data,
            "s": serial
        })

    # This will later be used to add author metadata, channel
    # metadata and a few other cool stuff.
    # @staticmethod
    # def generate_message(content, author=None):
    #     """
    #     Generate a message.
    #
    #     Parameters
    #     ----------
    #     content: str
    #         The actual content of the message.
    #     author: str
    #         Username of the author.
    #
    #     Returns
    #     -------
    #     message: dict
    #         The message.
    #     """
    #     return {
    #         "author": author,
    #         "content": content
    #     }

    async def broadcast(self, event_type, data=None, enable_serial=True):
        for ws in self.connected:
            if enable_serial:
                self.connected[ws]["s"] += 1
                event = self.generate_event(event_type, data, self.connected[ws]["s"])

            # Some event like heartbeat does not need serial.
            else:
                event = self.generate_event(event_type, data)

            await ws.send(event)
            del event

        # await asyncio.wait([ws.send(event) for ws in self.connected])

    # Generate the heartbeat to keep the websocket
    # connection alive.
    # TODO: close connection if client doesn't reply to heartbeat
    async def heartbeat(self):
        while True:
            await asyncio.sleep(self.HEART_BEAT_INTERVAL)

            try:
                await self.broadcast("HEARTBEAT", enable_serial=False)
            except Exception as e:
                print(e)

    # This coroutine handles individual websockets.
    # The individual clients are stored in 'connected'.
    async def ws_handler(self, websocket: websockets.WebSocketServerProtocol, path):
        # Register.
        self.connected[websocket] = {
            "id": uuid.uuid1(),
            # This will keep track of the number of events
            # we send to the client for current session.
            "s": 0
        }
        print(self.connected, path)

        try:
            # Send initial message
            ready_msg = {
                "message": "Welcome to arc! This is the websocket gateway. Have a nice day!",
            }
            await websocket.send(self.generate_event("HELLO", ready_msg, 0))
            del ready_msg

            # TODO: maybe delete some unwanted variables?
            while True:
                message = await websocket.recv()
                try:
                    parsed = json.loads(message)
                    # if parsed["type"] == "POST_MESSAGE":
                    #     gen_msg = self.generate_message(parsed["content"], parsed["author"])

                    print("POST_MESSAGE: {}".format(parsed["data"]))
                    await self.broadcast(parsed["type"], parsed["data"])

                except Exception as e:
                    print(e)

        except websockets.exceptions.ConnectionClosed as e:
            print(e, e.code, e.reason)

        finally:
            self.connected.pop(websocket)
            print(self.connected)

    def run(self):
        """
        This is a blocking call.
        """
        self.loop.create_task(self.heartbeat())
        start_server = websockets.serve(self.ws_handler, "0.0.0.0", 5555, loop=self.loop)
        self.loop.run_until_complete(start_server)
        self.loop.run_forever()

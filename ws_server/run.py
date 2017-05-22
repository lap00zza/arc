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

connected = []

async def handler(websocket, path):
    global connected

    # Register.
    connected.append(websocket)
    print(connected, path)

    try:
        # Send initial message
        await websocket.send(json.dumps({
            "event": "ready",
            "data": "Welcome to arc."
        }))

        while True:
            message = await websocket.recv()
            print("< {}".format(message))

            await asyncio.wait([ws.send(message) for ws in connected])
            print("> {}".format(message))

    except websockets.exceptions.ConnectionClosed as e:
        print(e, e.code, e.reason)

    finally:
        connected.remove(websocket)
        print(connected)

start_server = websockets.serve(handler, "0.0.0.0", 5555)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

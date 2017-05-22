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

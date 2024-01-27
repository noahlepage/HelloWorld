import asyncio
import websockets 
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)




from User import *

def which_user_is_this(data) :
    # this part simply user the ai model to figure out what user this is 

    current_user = User()

    return current_user




async def audio_handler(websocket, path):
    while True:
        data = await websocket.recv()
        # Process audio data (perform voice recognition, etc.)
        print("Received audio data:", data)
        # current_user = which_user_is_this(data)

        response_data = "Recognition result: Hello, World!"
        await websocket.send(response_data)



# "localhost", 8765 -> if everything is runing locally 
# your-backend-ip-or-domain -> if we are running something on a server 
start_server = websockets.serve(audio_handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

    

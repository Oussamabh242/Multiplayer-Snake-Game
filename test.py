# i thoght that i can run two seperate instances of the game 
# but it did not work 
# I am gonna mimic how the initial pygame instance work but console mode

# 5hrs later : i am wrong i was blocking the server with one socket

import time
import websockets 
import asyncio
import json

uri = 'ws://localhost:8765'
async def send(ws) :
        await ws.send('sup')

async def test():
    async with websockets.connect(uri) as ws :        
     
        while True :
            res = await ws.recv()
            try :
                res = json.loads(res)
                print(res) 
                break 
            except Exception as e :
                pass
        running = True 
        while running :

            await send(ws)
            await asyncio.sleep(0.1) 
    

asyncio.run(test())

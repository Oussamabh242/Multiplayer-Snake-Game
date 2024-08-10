# i thoght that i can run two seperate instances of the game 
# but it did not work 
# I am gonna mimic how the initial pygame instance work but console mode

import time
import websockets 
import asyncio

uri = 'ws://localhost:8765'
async def send(ws) :
        await ws.send('sup')

async def test():
    async with websockets.connect(uri) as ws :        
         running = True 
         while running :

            await send(ws)
            time.sleep(0.1) 
    

asyncio.run(test())

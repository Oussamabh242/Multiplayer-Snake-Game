import asyncio
import websockets 

rooms  = {
    'sup': {
       
        'food' : [200 , 300 , 20 , 20]
    }
}

async def hello(websocket) :
    rooms['sup'][websocket.id] = websocket
    print(len(rooms['sup']))
    while len(rooms['sup']) <3:
        pass
    while True :
        msg = await websocket.recv()
        print('recived ' + msg)

async def main():
    async with websockets.serve(hello , 'localhost' ,8765 ):
        await asyncio.Future()

if __name__ == '__main__' :
    print('listenning  ... ')
    asyncio.run(main())

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
    await websocket.send(str(len(rooms['sup'])))  
    if len(rooms['sup']) >= 3 :
        print(rooms)
        await broadcast('start' , rooms['sup'])
    while True :
        msg = await websocket.recv()
        print('recived ' + msg)


async def broadcast(msg , room) :
    for thing in room.keys() :
        if thing!= 'food' :
            await room[thing].send(msg)
            print(f'sent to {thing}')


async def main():
    async with websockets.serve(hello , 'localhost' ,8765 ):
        await asyncio.Future()



if __name__ == '__main__' :
    print('listenning  ... ')
    asyncio.run(main())

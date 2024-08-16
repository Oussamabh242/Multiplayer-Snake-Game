import asyncio
import websockets 
import random
import json

def generate_food_position(min_x, max_x, min_y, max_y):
    x = random.randint(min_x, max_x)
    y = random.randint(min_y, max_y)
    return [x, y, 20, 20]

rooms  = {
    # 'sup': {
    #
    #     'food' : generate_food_position(20, 580, 20, 380)
    # }
}



def collide(a , b , width):
    return (abs(a[0] - b[0]) < width and
            abs(a[1] - b[1]) < width)
def collides(a , b , food ) :
    head_to_head = collide(a[0] , b[0] ,30) ;
    head_to_food = collide(a[0] , food ,25  ) 
    head_to_body = False 
    this_head = a[0]
    for part in b :
        if collide(this_head , part  ,30) :
            head_to_body = True 
            break 

    return (head_to_head , head_to_body , head_to_food)

def formulate_response(id , oid , food , roomName) :
    this= rooms[roomName][id]['pos']
    other= rooms[roomName][oid]['pos']
    hh , hb , hf = collides(this ,other ,food)
    act = 'None'
    if hh :
        act = 'shrink' 
        rooms[roomName][id]['pos'] = initPlayer()
        rooms[roomName][id]['score'] =0 
        # rooms[roomName][oid]['pos'] = initPlayer()
        # rooms[roomName][oid]['respawn'] = True

    elif hb :
        act = 'shrink' 
        rooms[roomName][id]['pos'] = initPlayer()
        rooms[roomName][id]['score'] = 0   
    elif hf :
        act = 'grow'
        rooms[roomName]['food'] =  generate_food_position(20, 580, 20, 380) 
        rooms[roomName][id]['score']+=1
    return  {
        'act' : act , 
        'opp' : rooms[roomName][oid]['pos'] , 
        'my'  : rooms[roomName][id]['pos'] ,
        'food': rooms[roomName]['food'] ,
        'my_score' : rooms[roomName][id]['score'] ,
        'other_score' : rooms[roomName][oid]['score']
    }




def initPlayer():
    return [[random.randint(30 , 600 ) , random.randint(30 , 400 ) , 30 , 30 ]] 


async def hello(websocket) :
    handshake = await websocket.recv()
    handshake = json.loads(handshake) 
    # rooms['sup'][websocket.id] = {
    #     'socket' : websocket ,
    #     'pos' : initPlayer() , 
    #     'respawn' : False ,
    #     'score' : 0
    # }
    print(handshake) 
        
    roomName = handshake["room"]
    if handshake['choice'] == 1 :
        rooms[roomName] = {}
        rooms[roomName]['food'] =generate_food_position(30 ,570 ,30 ,370)
    
    rooms[roomName][websocket.id] = {
            'socket' : websocket , 
            'pos' : initPlayer() , 
            'respawn' : False ,
            'score' :0
    }

    print(rooms[roomName] , len(rooms[roomName]))

    if len(rooms[roomName]) >= 3 :
        await broadcast(rooms[roomName])
    id = websocket.id
    
    while True :
        room = rooms[roomName]
        this_pos = await websocket.recv()
        
        ## synchrnisation issue with this 
        ## after couple of times they collide head to head
        ## the cordinates shown on the screen aren't same 
        ## as the server 

        if room[id]['respawn']==True :
            rooms[roomName][id]['respawn'] = False
             

            # generate response :
            response = {
                'act' :  'shrinkall', 
                'my'  :  room[id]['pos']  , 
                'opp' :  get_other_pos(get_other_id(id ,room),room),
                'food': room['food']
            } 
            await websocket.send(json.dumps(response))

        else :  
            #########  IF NOT HEAD TO HEAD COLLISON ######
            this_pos = json.loads(this_pos)
            
            rooms[roomName][id]['pos'] = this_pos['pos']
            rooms[roomName][id]['len'] = this_pos['len']
            
            
            other_id = get_other_id(id , room)
            food = room['food']
            response = formulate_response(id ,other_id ,food  ,roomName)  
            

        await websocket.send(json.dumps(response))

def get_other_id(id , room) :
    for thing in room.keys():
        if thing != 'food' and thing != id :
            return thing
def get_other_pos(id , room) : 
    return room[id]['pos']

def other_pos(id , room):
    pos = {}
    for thing in room.keys():
        if thing != id and thing!='food' :
            pos['opp'] = room[thing]['pos']
    pos['food'] = room['food'][0:2]
    return pos

async def broadcast(room) :
    for thing in room.keys() :
        if thing!= 'food' :
            init = {
                'my' : room[thing]['pos'] , 
                'opp' : room[get_opp(thing, room)]['pos'] ,
                'food': room['food']
            }
            await room[thing]['socket'].send(json.dumps(init))

def get_opp(id  , room) :
     for thing in room.keys() :
        if thing!= 'food' and thing != id:
            return thing
 

async def main():
    async with websockets.serve(hello , 'localhost' ,8765 ):
        await asyncio.Future()



if __name__ == '__main__' :
    print('listenning  ... ')
    asyncio.run(main())

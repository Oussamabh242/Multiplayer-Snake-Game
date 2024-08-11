import pygame 
import typing
import math
from objects import Food , Object , Player , LinkedList
import time
import websockets 
import asyncio
import json

print('supppp')
uri = 'ws://localhost:8765'
async def send(ws) :

        await ws.send('sup')
player = 1 
opp = 1 
food = 1
def init(obj) :
    print(obj)
    player = Player(*obj['my'][0])
    opp = Player(*obj['opp'][0] )
    food = Food(*obj['food'])
    return (player , opp , food)

async def main():
    async with websockets.connect(uri) as ws :
        
        res = {}
        while True :
            res = await ws.recv()
            try :
                res = json.loads(res)
                print(res) 
                break 
            except Exception as e :
                pass
        player , opp , food = init(res) 
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        clock = pygame.time.Clock()
        running = True

        dt = 0
        # food : Food = Food(200 , 300 , 20 , 20)
        #
        # player = Player(300 , 300 , 30 , 30)
        # player.add()
        # player.add()
        # player.add()

        while running :
            print(player.length)
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    running = False 
            screen.fill("purple")
            my_pos = {
                'pos' : player.get_pos() , 
                'len' : player.length
            }
            await ws.send(json.dumps(my_pos))
            response = await ws.recv()
            response = json.loads(response)

            food.reset(*response['food'][0:2] )
            if response['act'] == 'grow' :
                player.add()
                food.render(screen , 'green')

            elif response['act'] == 'shrinkall' :
                player.shrink(*response['my'][0][0:2])
                opp.shrink(*response['opp'][0][0:2])
                food.render(screen , 'green')
            elif response['act'] == 'shrink' :
                player.shrink(*response['my'][0][0:2])

                food.render(screen , 'green')
            else :
                opp.setall(response['opp'])

                food.render(screen , 'green')
                
            
            pygame.display.flip()  

            food.render(screen , 'green')
            player.render_all(screen, 'red')
            food.render(screen , 'green')
            # opp.put(other_pos['opp'][0][0] , other_pos['opp'][0][1])
            opp.render_all(screen , 'blue')
            keys = pygame.key.get_pressed()
            changed = player.change_direction(keys)
            if not changed :
                player.move(screen, dt)
            food.render(screen , 'green')
            # player.self_collide()
            # if player.collide(food):
            #     food.positionize(screen)
            #     player.add()
            
            pygame.display.flip()  
            food.render(screen , 'green')
            dt = clock.tick(60) / 1000
            await asyncio.sleep(0.05) 
        pygame.quit()



asyncio.run(main())

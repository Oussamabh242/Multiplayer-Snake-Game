import pygame 
import typing
import math
from objects import Food , Object , Player , LinkedList
import time
import websockets 
import asyncio
import json

print('waiting ... ')
uri = 'ws://102.159.126.67:8765'

pygame.font.init() 
font = pygame.font.Font(None, 36)

# Render the text on a transparent surface


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
    async with websockets.connect(uri) as ws:
        res = {}
        while True:
            res = await ws.recv()
            try:
                res = json.loads(res)
                 
                break 
            except Exception as e:
                pass
        
        player, opp, food = init(res) 
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        clock = pygame.time.Clock()
        running = True
        dt = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            screen.fill("black")
            my_pos = {
                'pos': player.get_pos(), 
                'len': player.length
            }
            await ws.send(json.dumps(my_pos))
            response = await ws.recv()
            response = json.loads(response)

            # Update food position
            # food.reset(*response['food'][0:2])
            # food = Food(response['food'][0], response['food'][1] ,20 , 20)

            pygame.draw.rect(screen ,'green' ,pygame.Rect(response['food'][0] ,response['food'][1] ,20, 20))
            # Handle actions
            if response['act'] == 'grow':
                player.add()
            elif response['act'] == 'shrinkall':
                player.shrink(*response['my'][0][0:2])
                opp.shrink(*response['opp'][0][0:2])
            elif response['act'] == 'shrink':
                player.shrink(*response['my'][0][0:2])
            else:
                opp.setall(response['opp'])

            # Render everything once per frame 
            player.render_all(screen, 'red')
            opp.render_all(screen, 'blue')
           
            ## score
            ## x | y => x you , y opponent
            text = font.render(f'{response["my_score"]} | {response["other_score"]}', True, (255, 255, 255))

            screen.blit(text, (0, 0)) 
            pygame.display.flip()
            
            keys = pygame.key.get_pressed()
            changed = player.change_direction(keys)
            if not changed:
                player.move(screen, dt)
            
            dt = clock.tick(60) / 1000
            # await asyncio.sleep(0.05)
        
        pygame.quit()



asyncio.run(main())

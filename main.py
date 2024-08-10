import pygame 
import typing
import math
from objects import Food , Object , Player , LinkedList
import time
import websockets 
import asyncio

print('supppp')
uri = 'ws://localhost:8765'
async def send(ws) :

        await ws.send('sup')

async def main():
    async with websockets.connect(uri) as ws :
        
        pygame.init()
        screen = pygame.display.set_mode((600, 400))
        clock = pygame.time.Clock()
        running = True

        dt = 0
        food : Food = Food(200 , 300 , 20 , 20)

        player = Player(300 , 300 , 30 , 30)
        player.add()
        player.add()
        player.add()

        while running :
            await send(ws)
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    running = False 
            screen.fill("purple")

            food.render(screen , 'green')
            player.render_all(screen, 'red')
            keys = pygame.key.get_pressed()
            changed = player.change_direction(keys)
            if not changed :
                player.move(screen, dt)
            player.self_collide()
            if player.collide(food):
                food.positionize(screen)
                player.add()
            
            pygame.display.flip()  

            dt = clock.tick(60) / 1000
            time.sleep(0.1) 
        pygame.quit()



asyncio.run(main())

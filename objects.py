import time
from typing import Optional
import pygame
from random import randint
from math import sqrt , pow

availableDirections = {
    'LEFT' : ['UP' , 'DOWN'],
}

class Object :
    def __init__(self , x : float , y :float ,  width:int , height :int):

        ####################################
        #  init object's size and postion  #           
        ####################################
        self.x = x
        self.y = y 
        self.height = height
        self.width = width
  
    def render(self , screen , color) :
        pygame.draw.rect(screen ,color ,pygame.Rect(self.x , self.y , self.width , self.height))


class Food(Object) :
    def __init__(self, x: float, y: float, width: int, height: int):
        super().__init__(x, y, width, height) 

    def positionize(self , screen) :
        self.x = randint(20 , screen.get_width()-20)
        self.y = randint(20 , screen.get_height()-20)
    def reset(self ,x , y) :
        print('changeing ... ' , x , y) 
        self.x = x  
        self.y = y
        

class Player(Object) :
    color = 'red'
    def __init__(self, x: float, y: float, width: int, height: int):
        super().__init__(x, y, width, height)
        self.next = None
        self.prev = None
        self.tail = self
        self.direction = 'LEFT'
        self.length = 1
    def change_direction(self, keys):
        changed = False
        if self.direction in ['LEFT', 'RIGHT']:
            if keys[pygame.K_w] and self.direction != 'DOWN':
                self.direction = 'UP'
                changed = True
            elif keys[pygame.K_s] and self.direction != 'UP':
                self.direction = 'DOWN'
                changed = True
        elif self.direction in ['UP', 'DOWN']:
            if keys[pygame.K_a] and self.direction != 'RIGHT':
                self.direction = 'LEFT'
                changed = True
            elif keys[pygame.K_d] and self.direction != 'LEFT':
                self.direction = 'RIGHT'
                changed = True
        return changed   
    def move(self, screen, dt):
        speed = 150 * dt 
        if self.direction == 'UP':
            self.move_all(screen, 0, -speed)
        elif self.direction == 'DOWN':
            self.move_all(screen, 0, speed)
        elif self.direction == 'LEFT':
            self.move_all(screen, -speed, 0)
        elif self.direction == 'RIGHT':
            self.move_all(screen, speed, 0)
    def bound(self , screen) :
        if self.y < 0  :
            self.y = screen.get_height()
        if self.y > screen.get_height() :
            self.y = 0

        if self.x < 0  :
            self.x = screen.get_width()
        if self.x > screen.get_width() :
            self.x = 0
    def get_pos(self) :
        arr = []
        current = self 
        while current :
            arr.append([current.x , current.y])
            current = current.next
        return arr
        

    def move_all(self, screen, dx, dy):
        # Store old positions
        old_positions = []
        current = self
        while current:
            old_positions.append((current.x, current.y))
            current = current.next
        
        # Move head
        self.x += dx
        self.y += dy
        self.bound(screen)
        # self.render(screen, self.color)
        
        # Move body
        current = self.next
        i = 0
        while current:
            current.x, current.y = old_positions[i]
            current.bound(screen)
            # current.render(screen, self.color)
            current = current.next
            i += 1           

    def add(self ):
        new = Player(self.tail.x+self.tail.width+10 ,self.tail.y ,self.tail.width , self.tail.height)
        new.prev = self.tail 
        self.tail.next = new
        self.tail = new
        self.length +=1

    def shrink(self , x , y):
        self.next = None 
        self.tail = self 
        self.length = 1
        self.x = x 
        self.y = y
    def setall(self , arr) :

        self.x = arr[0][0]
        self.y = arr[0][1]
        self.next = None
        self.tail = self
        current = self 
        for i in range(1 , len(arr)) :
            x = arr[i][0]
            y = arr[i][1]
            new = Player(x ,y ,self.width , self.height)
            current.next = new 
            self.tail = new
            current = current.next 




    def self_collide(self):
        ## i think if the length is less than 5 there will be no self collision 
        ## so i will be checking form the 5th node ...
        head = self 
        current = self 
        for _ in range(5) :
            if not current :
                return 
            current = current.next
        while current :
            if head.collide(current):
                self.shrink()
                return 
            current = current.next

    def render_all(self, screen, color):
        current = self        
        if self.next : 
            self.render(screen,'white')
            current = self.next
        while current :
            current.render(screen , color) 
            current = current.next

    def collide(self, obj:Object):
        return (abs(self.x - obj.x) < (self.width + obj.width) / 2 and
                abs(self.y - obj.y) < (self.height + obj.height) / 2)
    def put(self , x , y):
        self.x  = x 
        self.y = y
        

class LinkedList:
    def __init__(self, head: Player, next: Optional['LinkedList'] = None, gap: int = 5):
        self.head = head
        self.next = next
        self.gap = gap

    def render_all(self, screen, color):
        current = self
        while current:
            current.head.render(screen, color)
            current = current.next

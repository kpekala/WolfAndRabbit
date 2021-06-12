# Simple pygame program

# Import and initialize the pygame library
from random import random, randrange
from typing import List

import pygame

SIZE_X = 20
SIZE_Y = 20

class Animal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class BaseWolf(Animal):
    def __init__(self, x, y):
        Animal.__init__(self,x,y)
        self.hp = 1
        self.is_male = True


class Node:
    def __init__(self):
        self.rabbits_count = 0
        self.wolves = []



male_wolves = []
female_wolves = []
rabbits = []


def draw(screen, objects):
    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    pygame.display.flip()

def animals():
    return male_wolves + female_wolves + rabbits

def random_direction(x, y):
    dir_arr = [(-1,-1), (-1,0), (-1, 1), (0, -1), (0,0), (0,1), (1,-1), (1,0),(1,1)]
    dx, dy =dir_arr[randrange(0,len(dir_arr))]
    if not 0 <= x + dx < SIZE_X:
        dx = -dx
    if not 0 <= y + dy < SIZE_Y:
        dy = -dy
    return dx, dy

def move_rabbits(objects: List[List[Node]]):
    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            node = objects[y][x]
            rabbits_count = node.rabbits_count
            for _ in range(rabbits_count):
                dx, dy = random_direction(y, x)
                node.rabbits_count -= 1
                objects[y+dy][x+dx].rabbits_count += 1


def reproduce_rabbits(objects):
    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            node = objects[y][x]
            rabbits_count = node.rabbits_count
            for _ in range(rabbits_count):
                node.rabbits_count += int(random() <= 0.2)



def update_rabbits(objects: List[List[Node]]):
    move_rabbits(objects)
    reproduce_rabbits(objects)





def main():
    pygame.init()
    screen = pygame.display.set_mode([500, 500])

    objects = [[Node() for x in range(SIZE_X)] for y in range(SIZE_Y)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update_rabbits()
        draw(screen, animals())


    pygame.quit()


main()

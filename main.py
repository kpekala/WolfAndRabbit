from random import random, randrange
import random
import threading
from time import sleep
from typing import List

import pygame

SIZE_X = 20
SIZE_Y = 20


class Animal:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class BaseWolf(Animal):
    def __init__(self, x, y, is_male):
        Animal.__init__(self, x, y)
        self.hp = 1
        self.is_male = is_male


class Node:
    def __init__(self):
        self.rabbits_count = 0
        self.wolves = []


male_wolves = []
female_wolves = []
rabbits = []


def main():
    pygame.init()
    screen = pygame.display.set_mode([600, 600])

    objects = [[Node() for x in range(SIZE_X)] for y in range(SIZE_Y)]

    # input_thread = threading.Thread(target=input_handler)
    # input_thread.start()

    #add_random_rabbits(objects, 10)
    add_random_wolves(objects, 7)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update_rabbits(objects)
        update_wolves(objects)
        draw(screen, objects)
        sleep(0.3)

    pygame.quit()



def draw(screen, objects):
    screen.fill((0, 0, 0))

    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            node = objects[y][x]
            green = min(node.rabbits_count * 30, 255)
            pygame.draw.rect(screen, (0, green, 0), (x * 30, y * 30, 30, 30))

            red = min(len(node.wolves) * 30, 255)
            pygame.draw.circle(screen, (red, 0, 0), (x * 30 + 15, y * 30 + 15), 15)

    pygame.display.flip()


def add_random_rabbits(objects, count):
    for _ in range(count):
        x, y = randrange(0, SIZE_X), randrange(0, SIZE_Y)
        objects[y][x].rabbits_count += 1

def add_random_wolves(objects, count):
    for _ in range(count):
        x, y = randrange(0, SIZE_X), randrange(0, SIZE_Y)
        wolf = BaseWolf(x, y, bool(random.getrandbits(1)))
        objects[y][x].wolves.append(wolf)

# def input_handler():
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#         sleep(1)


def animals():
    return male_wolves + female_wolves + rabbits


def get_dir_arr(): return [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]


def random_direction(x, y):
    dir_arr = get_dir_arr()
    dx, dy = dir_arr[randrange(0, len(dir_arr))]
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
                dx, dy = random_direction(x, y)
                node.rabbits_count -= 1
                objects[y + dy][x + dx].rabbits_count += 1


def reproduce_rabbits(objects):
    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            node = objects[y][x]
            rabbits_count = node.rabbits_count
            for _ in range(rabbits_count):
                node.rabbits_count += int(random.random() <= 0.2)


def update_rabbits(objects: List[List[Node]]):
    move_rabbits(objects)
    reproduce_rabbits(objects)


def is_rabbit_nearby(objects: List[List[Node]], wolf: BaseWolf):
    for dx, dy in get_dir_arr():
        if 0 <= wolf.x + dx < SIZE_X and 0 <= wolf.y + dy < SIZE_Y and \
                objects[wolf.y + dy][wolf.x + dx].rabbits_count > 0:
            return True, dx, dy
    return False, -1,-1


def is_female_nearby(objects: List[List[Node]], wolf):
    for dx, dy in get_dir_arr():
        if 0 <= wolf.x + dx < SIZE_X and 0 <= wolf.y + dy < SIZE_Y:
            wolves = objects[wolf.x + dx][wolf.y + dy].wolves
            female = next(iter([wolf for wolf in wolves if not wolf.is_male]), None)
            if female:
                return female


def move_wolves(objects: List[List[Node]]):
    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            node = objects[y][x]
            old_wolves = node.wolves.copy()
            for wolf in old_wolves:
                print(wolf.hp)
                is_rabbit, dx, dy = is_rabbit_nearby(objects, wolf)
                if is_rabbit:
                    objects[wolf.y + dy][wolf.x + dx].rabbits_count -= 1
                    wolf.hp += 1
                else:
                    wolf.hp -= 0.1
                    hunting = False
                    if wolf.is_male:
                        female = is_female_nearby(objects, wolf)
                        if female:
                            hunting = True
                            new_wolf = BaseWolf(female.x, female.y, bool(random.getrandbits(1)))
                            objects[female.y][female.x].wolves.append(new_wolf)
                            dx, dy = new_wolf.x - wolf.x, new_wolf.y - wolf.y

                    if not hunting:
                        dx, dy = random_direction(wolf.x, wolf.y)

                wolf.x += dx
                wolf.y += dy

                if not (dx, dy) == (0,0):
                    node.wolves.remove(wolf)
                    objects[wolf.y][wolf.x].wolves.append(wolf)


def remove_dead_wolves(objects):
    for y in range(SIZE_Y):
        for x in range(SIZE_X):
            node = objects[y][x]
            node.wolves = [wolf for wolf in node.wolves if wolf.hp > 0]


def update_wolves(objects):
    remove_dead_wolves(objects)
    move_wolves(objects)


if __name__ == '__main__':
    main()

import pygame
import pygame.freetype

SIZE_X = 20
SIZE_Y = 20



class Drawer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.freetype.SysFont(pygame.font.get_default_font(), 50)

    def draw(self, objects, turn):
        self.screen.fill((0, 0, 0))

        for y in range(SIZE_Y):
            for x in range(SIZE_X):
                node = objects[y][x]
                #render rabbits
                green = min(node.rabbits_count * 30, 255)
                pygame.draw.rect(self.screen, (0, green, 0), (x * 30, y * 30, 30, 30))

                #render wolves
                red = min(len(node.wolves) * 30, 255)
                if red != 0:
                    pygame.draw.circle(self.screen, (red, 0, 0), (x * 30 + 15, y * 30 + 15), 15)

                #render number od turns
                self.font.render_to(self.screen,(0,0),str(turn),(255,255,255))



        pygame.display.flip()
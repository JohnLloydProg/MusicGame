import pygame
import os


class Beat:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, speed):
        self.x -= speed

    def draw(self, win):
        pygame.draw.rect(win, (192, 192, 192), (self.x+44, self.y-10, 2, 110))
        win.blit(pygame.image.load(os.curdir+"/images/beat_img.png"), (self.x, self.y))

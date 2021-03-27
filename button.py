import pygame


class Button:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.font = pygame.font.SysFont("None", 40)

    def inside(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.x+300 > mouse_x > self.x and self.y+75 > mouse_y > self.y:
            return True

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class MusicButton(Button):
    def __init__(self, x, y, image, name):
        Button.__init__(self, x, y, image)
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        win.blit(self.font.render(self.name, True, (255, 255, 255)), (self.x + 25, self.y + 25))

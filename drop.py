import pygame
from pygame.sprite import Sprite
import random


class Drop(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        
        self.screen_rect = game.screen.get_rect()
        self.image = pygame.image.load("images/{}.png".format('coin'))
        self.rect = self.image.get_rect()
        
        rect_x = random.randint(0, self.settings.screen_width-self.rect[-1])
        self.rect.x = rect_x
        self.y = float(self.rect.y)
        
        
    def update(self):
        self.y += self.settings.drop_speed
        self.rect.y = self.y

class Bomb(Sprite):
    def __init__(self, gold_game):
        super().__init__()
        self.screen = gold_game.screen
        self.settings = gold_game.settings
        
        self.screen_rect = gold_game.screen.get_rect()
        self.image = pygame.image.load("images/{}.png".format('bomb'))
        self.rect = self.image.get_rect()
        
        rect_x = random.randint(0, self.settings.screen_width-self.rect[-1])
        self.rect.x = rect_x
        self.y = float(self.rect.y)
        
        
    def update(self):
        self.y += self.settings.drop_speed
        self.rect.y = self.y
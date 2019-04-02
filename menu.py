import pygame
import random

from boom import Boom
from tank import Superone
from map import Wall

class Menu(pygame.sprite.Sprite):
    def __init__(self, type , x, y, tg):
        pygame.sprite.Sprite.__init__(self)
        self.tg = tg
        self.type = type
        self.unlock = True
        self.images = self.tg.images.menu 
        self.image = self.images[self.type][0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y

    def update(self, show_menu, event = None):
        if self.type in show_menu:
            self.unlock = True
            if self.type != 4 and self.type != 5:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.image = self.images[self.type][1]
                else:
                    self.image = self.images[self.type][0]
        else:
            self.unlock = False
            self.image = self.images[self.type][2]
        if event is not None:
            self.mouse(event)

    def mouse(self, event):
        if self.unlock and self.rect.collidepoint(event.pos) and event.button is 1:
            if self.type is 0:
                self.tg.is_show_menu = False
                self.tg.is_run = True
            elif self.type is 1:
                self.tg.is_show_menu = False
            elif self.type is 2:
                self.tg.is_show_checkpoint = not self.tg.is_show_checkpoint
            elif self.type is 3:
                self.tg.quit()
            elif self.type is 4:
                self.tg.is_mixer = not self.tg.is_mixer
                self.image = self.images[self.type][int(not self.tg.is_mixer)]
            elif self.type is 5:
                self.tg.is_music = not self.tg.is_music
                self.image = self.images[self.type][int(not self.tg.is_music)]
                if not self.tg.is_music and pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                elif self.tg.is_music and self.tg.is_run:
                    pygame.mixer.music.play()

class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, type, x, y, tg):
        pygame.sprite.Sprite.__init__(self)
        self.tg = tg
        self.type = type
        self.images = self.tg.images.checkpoint
        self.image = self.images[self.type][0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self, event = None):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.images[self.type][1]
        else:
            self.image = self.images[self.type][0]
        if event is not None:
            self.mouse(event)

    def mouse(self, event):
        if self.tg.is_show_checkpoint and self.rect.collidepoint(event.pos) and event.button is 1:
            self.tg.edit_checkpoint = self.type
            self.tg.is_show_checkpoint =False
            self.tg.is_show_menu = False
            self.tg.is_edit_map = True
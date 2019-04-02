import pygame
from pygame.locals import *
import pickle

class Map(object):
    def __init__(self,tg):
        self.tg = tg
        self.wall_type = 5
        self.init()

    def init(self):
        self.start_pos = None
        self.end_pos = None
        self.button = None

    def update(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.mouse_down(event)
        if event.type == MOUSEBUTTONUP:
            self.mouse_up(event)
        if event.type == MOUSEMOTION:
            if self.start_pos is not None:
                self.draw_rect(event.pos)
        if event.type == KEYDOWN:
            if event.key == K_1:
                self.wall_type = 0
            elif event.type ==K_2:
                self.wall_type = 1
            elif event.key == K_3:
                self.wall_type = 2
            elif event.key == K_4:
                self.wall_type = 3
            elif event.key == K_5:
                self.wall_type = 5
            elif event.key == K_ESCAPE:
                self.tg.is_edit_map = False
                self.tg.is_show_menu = True
                self.save()

    def cursor(self):
        pos = pygame.mouse.get_pos()
        self.tg.screen.blit(self.tg.images.wall[self.wall_type], pos)

    def save(self):
        map_list = []
        for wall in self.tg.maps:
            map_list.append((wall.type, wall.x, wall.y))
        self.tg.map_data[self.tg.edit_checkpoint]['data'] = tuple(map_list)
        with open('map.pkl', 'wb')as f:
            pickle.dump(self.tg.map_data, f)
        self.tg.maps.empty()
        self.tg.walls.empty()
        self.tg.init_wall()

    def mouse_down(self,event):
        if event.button is 1:
            self.start_pos = event.pos
            self.button = 1
        elif event.button is 3:
            self.start_pos = event.pos
            self.button = 3
    def mouse_up(self, event):
        if event.button is 1:
            self.end_pos = event.pos
            self.button = 1
        elif event.button is 3:
            self.end_pos = event.pos
            self.button = 3
        self.operation()

    def draw_rect(self, pos):
        self.tg.select_rect  = pygame.Rect(self.rect(pos))

    def rect(self, pos):
        pos_x = self.start_pos[0], pos[0]
        pos_y = self.start_pos[1], pos[1]
        x = min(pos_x)
        y = min(pos_y)
        w = abs(self.start_pos[0] - pos[0])
        h = abs(self.start_pos[1] - pos[1])
        return x, y, w, h

    def operation(self):
        if self.start_pos is not None and self.end_pos is not None:
            self.tg.select_rect = None
            select = Select(*self.rect(self.end_pos))
            collide_list = pygame.sprite.spritecollide(select, self.tg.maps, False)
            for map in collide_list:
                if self.button == 1:
                    map.image = map.images[self.wall_type]
                    map.type = self.wall_type

                elif self.button == 3:
                    map.image = map.images[5]
                    map.type = 5
            self.init()

class Select(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, h])
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

class Wall(pygame.sprite.Sprite):
    def __init__(self, tg, wall):
        pygame.sprite.Sprite.__init__(self)
        self.tg = tg
        self.type, self.x, self.y = wall
        self.images = self.tg.images.wall
        self.image = self.images[self.type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.mask = pygame.mask.from_surface(self.image)
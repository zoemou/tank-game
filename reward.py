import pygame
import random
from boom import Boom
from tank import Superone,Tank
from map import Wall

class Reward(pygame.sprite.Sprite):
    def __init__(self, tg):
        pygame.sprite.Sprite.__init__(self)
        self.tg = tg
        self.type = random.randrange(len(self.tg.images.reward))
        self.images = self.tg.images.reward
        self.image = self.images[self.type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.randrange(self.tg.width - 40), random.randrange(self.tg.height - 40)
        self.live = 500

    def update(self):
        if self.live < 0:
            self.tg.rewards.remove(self)
        elif self.live <160:
            if self.live % 5 == 0 :
                self.image = self.tg.images.blank
            else:
                self.image = self.images[self.type]
            self.live -= 1
        else:
            self.live -= 1
        self.collide_tank()

    def collide_tank(self):
        collide_list = pygame.sprite.spritecollide(self,self.tg.tanks,False)
        for tank in collide_list:
            if tank.type > 0:
                if self.tg.is_mixer:
                    self.tg.music.get_reward.play()
                if self.type is 0:
                    self.life_add(tank)
                elif self.type is 1:
                    self.get_box()
                elif self.type is 2:
                    self.boom_all()
                elif self.type is 3:
                    self.get_super(tank)
                self.tg.rewards.remove(self)

    def life_add(self, tank):
        if tank.type is 1 and self.tg.player1_num < 5:
            self.tg.player1_num += 1
        if tank.type is 2 and self.tg.player2_num < 5:
            self.tg.player2_num += 1

    def get_box(self):
        for w in self.tg.home:
            self.tg.walls.add(Wall(self.tg, w))

    def boom_all(self):
        for tank in self.tg.tanks:
            if tank.type is 0:
                self.tg.booms.add(Boom(self.tg.images.boom, 'tank', tank, self.tg))
                tank.is_over()

    def get_super(self, tank):
        if not tank.is_super:
            tank.is_super = True
            self.tg.rewards.add(Superone(tank, self.tg))


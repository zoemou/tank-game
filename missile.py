import pygame
import random


class Missile(pygame.sprite.Sprite):
    def __init__(self, tank, tg):
        pygame.sprite.Sprite.__init__(self)
        self.tg = tg
        self.tank = tank
        self.type = self.tank.type
        self.dir = self.tank.ptdir
        self.img_num = self.tank.img_num
        self.images = self.tg.images.missile[self.img_num]
        self.image = self.images.get(self.dir)
        self.speed = self.tank.speed * 2
        self.rect = self.image.get_rect()
        self.rect.center = self.tank.rect.center
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.move_ip(self.move())
        self.hit_tank()
        self.hit_missile()
        self.hit_wall()
        self.out()

    def move(self):
        x, y = 0, 0
        if self.dir is self.tank.dirs[0]:
            y = -self.speed
        elif self.dir is self.tank.dirs[1]:
            y = self.speed
        elif self.dir is self.tank.dirs[2]:
            x = -self.speed
        elif self.dir is self.tank.dirs[3]:
            x = self.speed
        return x, y

    def hit_tank(self):
        collide_list = pygame.sprite.spritecollide(self,self.tg.tanks,False,pygame.sprite.collide_mask)
        for tank in collide_list:
            if bool(tank.type) is not bool(self.type):
                self.tg.missiles.remove(self)
                tank.is_over()

    def hit_missile(self):
        collide_list = pygame.sprite.spritecollide(self,self.tg.missiles,False)
        for missile in collide_list:
            if bool(missile.type) is not bool(self.type):
                missile.kill()
                self.kill()

    def hit_wall(self):
        collide_list = pygame.sprite.spritecollide(self,self.tg.walls,False,pygame.sprite.collide_mask)
        for wall in collide_list:
            if wall.type is 0:
                self.tg.missiles.remove(self)
                self.tg.walls.remove(wall)
            elif wall.type is 3:
                self.tg.missiles.remove(self)
            elif wall.type is 4 and self.type is 0:
                self.tg.missiles.remove(self)
                self.tg.walls.remove(wall)
                self.tg.is_over = True

    def out(self):
        if self.rect.right > self.tg.width or self.rect.left < 0 or self.rect.bottom > self.tg.height or self.rect.top < 0:
            self.tg.missiles.remove(self)
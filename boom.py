import pygame

class Boom(pygame.sprite.Sprite):
    def __init__(self, images, name, tank, tg):
        pygame.sprite.Sprite.__init__(self)
        self.tg = tg
        self.tank = tank
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.tank.rect.center
        self.step = 0
        self.offset(name)

    def update(self):
        self.image = self.images[self.step // 4]
        if self.step == len(self.images) * 4 - 1:
            self.tg.booms.remove(self)
        else:
            self.step += 1

    def offset(self, name):
        if name == 'fire':
            if self.tank.ptdir is self.tank.dirs[0]:
                self.rect.centery -= self.tank.rect.width / 2
            elif self.tank.ptdir is self.tank.dirs[1]:
                self.rect.centery += self.tank.rect.width / 2
            elif self.tank.ptdir is self.tank.dirs[2]:
                self.rect.centerx -= self.tank.rect.height / 2
            elif self.tank.ptdir is self.tank.dirs[3]:
                self.rect.centerx += self.tank.rect.height / 2
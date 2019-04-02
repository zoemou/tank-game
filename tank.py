import random

import pygame
from pygame.locals import *

from boom import Boom
from missile import Missile


class Tank(pygame.sprite.Sprite):
    """
    坦克类，包括敌我双方坦克
        type 坦克类型，0为敌方坦克，1为英雄1号，2为英雄2号
    """

    def __init__(self, x, y, type, tg):
        pygame.sprite.Sprite.__init__(self)
        self.tg = tg
        self.type = type
        self.is_super = False # 无敌状态
        self.img_num = self.type if self.type > 0 else random.choice([0,3])
        self.images = self.tg.images.tank[self.img_num]
        self.image = self.images.get('up')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        # 坦克速度由主类通过难度和关卡计算
        self.speed = self.tg.player_tank_speed if self.type > 0 else self.tg.enemy_tank_speed
        self.dirs = 'up', 'down', 'left', 'right', 'stop'
        # 坦克方向
        self.dir = self.dirs[0 if self.type > 0 else 1]
        # 炮桶主向
        self.ptdir = self.dir
        # 敌方坦克每个方向移动步长
        self.step = random.randint(6, 20)
        self.x, self.y = self.rect.x, self.rect.y = x, y
        # 英雄坦克最大挂载子弹数量
        self.player_missile_max_number = 5
        self.enemy_missile_max_number = 0 #+ self.tg.difficult
        self.interval = 0
    # 重写精灵更新方法
    def update(self, key, event=None):
        #手柄
        if self.type is 1 and self.tg.joyin == True:
            self.is_super = True
            if self.tg.attack == 1:
                self.fire()
            if self.tg.dy == 1:
                self.dir = self.dirs[0]
            elif self.tg.dy == -1:
                self.dir = self.dirs[1]
            elif self.tg.dx == -1:
                self.dir = self.dirs[2]
            elif self.tg.dx == 1:
                self.dir = self.dirs[3]
            else:
                self.dir = self.dirs[4]
        # 如果坦克为英雄1号
        if self.type is 1 and self.tg.joyin == False:
            if event is not None and event.key == K_j or self.tg.attack == 1:
                # 按j键发射子弹
                self.fire()
            # 根据wasd键状态改变坦克方向
            if key[K_w] or self.tg.dy == 1:
                self.dir = self.dirs[0]
            elif key[K_s] or self.tg.dy == -1:
                self.dir = self.dirs[1]
            elif key[K_a] or self.tg.dx == -1:
                self.dir = self.dirs[2]
            elif key[K_d] or self.tg.dx == 1:
                self.dir = self.dirs[3]
            else:
                self.dir = self.dirs[4]
        if self.type is 2:
            # 如果坦克为英雄2号，小键盘4发子弹，方向键改变方向
            if event is not None and event.key == K_KP4:
                self.fire()
            if key[K_UP]:
                self.dir = self.dirs[0]
            elif key[K_DOWN]:
                self.dir = self.dirs[1]
            elif key[K_LEFT]:
                self.dir = self.dirs[2]
            elif key[K_RIGHT]:
                self.dir = self.dirs[3]
            else:
                self.dir = self.dirs[4]
        else:
            # 否则，敌方坦克调用自动改变方向的方法
            self.turn_dir()
        if self.dir is not self.dirs[4]:
            # 如果坦克不是停止状态，炮桶方向跟坦克方向
            self.ptdir = self.dir
        # 根据坦克方向改变坦克图片
        self.image = self.images.get(self.ptdir)
        self.out()
        self.collide_wall()
        self.collide_tank()
        self.load_missile()
        # 移动坦克
        self.rect.move_ip(self.move())

    # 根据坦克方向计算坦克移动量
    def move(self):
        self.x, self.y = self.rect.x, self.rect.y
        x, y = 0, 0
        if self.dir is self.dirs[0]:
            y = -self.speed
        elif self.dir is self.dirs[1]:
            y = self.speed
        elif self.dir is self.dirs[2]:
            x = -self.speed
        elif self.dir is self.dirs[3]:
            x = self.speed
        return x, y

    # 改变敌方坦克方向
    def turn_dir(self):
        if self.type is 0:
            if self.step > 0:
                self.step -= 1
            else:
                # 随机生成前进步数
                self.step = random.randint(6, 20)
                # 随机生成前进方向
                self.dir = self.dirs[random.choice([0,0,0,1,1,1,1,1,2,2,2,3,3,3,4,])]
            if random.randrange(40) > 38 - self.tg.difficult //2:
                self.fire()
        if self.type is 0:
            collide_list = pygame.sprite.spritecollide(self,self.tg.walls,False,pygame.sprite.collide_mask)
            for wall in collide_list:
                if wall.type != 1 :
                    self.dir_change()
        if self.type is 0:
            if self.rect.right > self.tg.width or self.rect.left < 0 or self.rect.bottom > self.tg.height or self.rect.top < 0:
                self.dir_change()
        if self.type is 0:
            for w in self.tg.home:
                collide_list = pygame.sprite.spritecollide(self, self.tg.walls, False)
                for wall in collide_list:
                    if w[1] == wall.x and w[2] == wall.y:
                        self.fire()


    def dir_change(self):
        if self.dir is self.dirs[0]:
            self.dir = self.dirs[random.choice([1,2,3])]
        elif self.dir is self.dirs[1]:
            self.dir = self.dirs[random.choice([0,2,3])]
        elif self.dir is self.dirs[2]:
            self.dir = self.dirs[random.choice([1,0,3])]
        elif self.dir is self.dirs[3]:
            self.dir = self.dirs[random.choice([1,2,0])]
    # 如果有子弹就就发子弹
    def fire(self):
        if self.type > 0:
            if self.player_missile_max_number > 0:
            # 生成一颗子弹
                self.tg.missiles.add(Missile(self, self.tg))
            # 生成一个子弹发射爆炸
                self.tg.booms.add(Boom(self.tg.images.fire, 'fire', self, self.tg))
                self.player_missile_max_number -= 1
                if self.tg.is_mixer:
                    self.tg.music.fire.play()
        else:
            if self.enemy_missile_max_number > 0:
                self.tg.missiles.add(Missile(self,self.tg))
                self.tg.booms.add(Boom(self.tg.images.fire, 'fire', self, self.tg))
                self.enemy_missile_max_number -= 1

    # 判断超出边界
    def out(self):
        if self.rect.right > self.tg.width:
            self.rect.right = self.tg.width
        elif self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > self.tg.height:
            self.rect.bottom = self.tg.height
        elif self.rect.top < 0:
            self.rect.top = 0

    # 每20帧挂载一发炮弹
    def load_missile(self):
        if self.interval > 50:
            self.interval = 0
        else:
            self.interval += 1
        if self.interval % 10 == 0 and self.player_missile_max_number < 5:
            # 到时间挂载子弹，并且可装载子弹还有空间，增加一颗子弹
            self.player_missile_max_number += 1
        if self.interval == 5 and self.enemy_missile_max_number < 1: #+ self.tg.difficult:
            self.enemy_missile_max_number += 1

    # 判断坦克是否挂了
    def is_over(self):
        self.tg.booms.add(Boom(self.tg.images.boom, 'tank', self, self.tg))
        if self.type > 0:
            if not self.is_super:
                if self.type is 1 and self.tg.player1_num > 0 or self.type is 2 and self.tg.player2_num > 0:
                    # 英雄1号或2号剩余坦克大于0，重置坦克位置
                    self.reset_pos()
                else:
                    # 否则移除坦克，并设置正在游戏中的英雄数量-1
                    self.tg.tanks.remove(self)
                    self.tg.player_num -= 1
        else:
            # 如果是敌方坦克，直接移除，并减小敌方剩余坦克数量，主类中会根据坦克剩余量和运行中坦克生成新坦克
            self.tg.tanks.remove(self)
            # self.tg.enemy_num -= 1
            if self.tg.is_mixer:
                # 播放音效
                self.tg.music.boom.play()

    # 重置英雄坦克
    def reset_pos(self):
        # 分别对英雄1号和2号坦克的位置进行重置，并减小坦克剩余量
        if self.type is 1:
            self.rect.x, self.rect.y = 400, 600
            self.tg.player1_num -= 1
        elif self.type is 2:
            self.rect.x, self.rect.y = 520, 600
            self.tg.player2_num -= 1

    # 坦克碰撞墙
    def collide_wall(self):
        collide_list = pygame.sprite.spritecollide(self, self.tg.walls, False, pygame.sprite.collide_mask)
        for wall in collide_list:
            if wall.type != 1 :
                # 除了碰到草墙，碰到其它墙坦克均停止前进
                self.stay()

    # 坦克之间互相碰撞检测
    def collide_tank(self):
        collide_list = pygame.sprite.spritecollide(self, self.tg.tanks, False, pygame.sprite.collide_mask)
        for tank in collide_list:
            if self is not tank:
                # 如果是同一方坦克，各自回到上一步的位置
                if bool(tank.type) is bool(self.type):
                    tank.stay()
                    self.stay()
                else:
                    tank.is_over()
                    self.is_over()
                if self.type is 0 and tank.type is 0:
                    if random.choice([0,1]) is 0:
                        self.dir_change()
                    else:
                        tank.dir_change()

    def stay(self):
        self.rect.x, self.rect.y = self.x, self.y

class Superone(pygame.sprite.Sprite):
    def __init__(self, tank, tg):
        pygame.sprite.Sprite.__init__(self)
        self.tg = tg
        self.tank = tank
        self.image = self.tg.images.super
        self.rect = self.tank.rect
        self.is_live = 500

    def update(self):
        self.rect = self.tank.rect
        if self.is_live == 0 :
            self.tank.is_super = False
            self.tg.rewards.remove(self)
        else:
            self.is_live -= 1

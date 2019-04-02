import pickle 
import sys,random

import pygame
from pygame.locals import *

from map import Map,Select,Wall
from menu import Menu,Checkpoint
from resource import Img, Music
from reward import Reward
from tank import Tank
from joystick import Joystick


class TankGame(object):
    #主类

    def __init__(self):
        #定义游戏窗口
        self.size = self.width, self.height = 960, 640
        #初始化游戏和一些内容
        pygame.init()
        #生成游戏窗口
        self.screen = pygame.display.set_mode(self.size)
        #载入资源
        self.images = Img()
        self.music = Music()
        self.map = Map(self)

        #设置窗口名
        pygame.display.set_caption('TankGame')
        #设置窗口图标
        pygame.display.set_icon(self.images.icon)
        #初始化声音
        pygame.mixer.init()
        #背景音乐
        pygame.mixer.music.load('music/music.wav')
        #设置音量
        pygame.mixer.music.set_volume(0.3)

        #定义坦克的type
        self.enemy, self.player1, self.player2 = 0, 1, 2
        #定义玩家坦克的生命值
        self.player1_num, self.player2_num = 5, 5
        #定义两个计数器用于手柄
        self.dx, self.dy= 0, 0
        self.attack = 0
        #加入的手柄
        self.joystick = Joystick(self)
        self.joyin = False
        #设置一些变量和开关
        #难度
        self.difficult = 1
        #关卡
        self.checkpoint = 0
        #编辑地图关卡
        self.edit_checkpoint = 0
        #定义地图数据
        self.map_data = None
        #编辑地图时候的方框
        self.select_rect = None
        #一些开关
        self.is_music = True
        self.is_mixer = True
        self.is_run = False
        self.is_over = False
        self.is_show_menu = True
        self.is_show_checkpoint = False
        self.is_edit_map = False
        self.is_win = False
        self.is_show_win = True
        #计时器
        self.step = 4000
        #道具计时器
        self.step_reward = 6000
        #实例化帧
        self.clock = pygame.time.Clock()
        self.load_map()
        self.init()


        #游戏初始化
    def init(self):
        self.init_args()
        self.init_wall()
        self.init_tank()
        self.init_menu()
        self.running()
        self.init_joystick()


    def init_joystick():
        self.joystick.init()
        self.joyin = False

    def init_args(self):
        #设置敌方坦克数量随游戏增加
        self.enemy_num = 15 + ((self.difficult + 1) * 3) * self.checkpoint
        #设置敌方坦克在场数
        self.enemy_show_num = 3 + self.difficult + ((self.checkpoint // 2) + 1)
        #设置坦克运动速度
        self.enemy_tank_speed = round(2 + (self.difficult + (self.checkpoint // 2) + 10) / 10)
        self.player_tank_speed = 8
        
        self.player_num = 2

        self.missiles = pygame.sprite.Group() #子弹图层
        self.tanks = pygame.sprite.Group() 
        self.booms = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.menus = pygame.sprite.Group()
        self.maps = pygame.sprite.Group()
        self.checkpoints = pygame.sprite.Group()
        self.rewards = pygame.sprite.Group()
        self.joystick = pygame.sprite.Group()


    def load_map(self):
        with open('map.pkl', 'rb')as f:
            self.map_data = pickle.load(f)


    def init_wall(self):
        self.home=(
            (0, 440, 580), (0, 440, 600), (0, 440, 620), (0, 460, 580), 
            (0, 480, 580), (0, 500, 580), (0, 500, 600), (0, 500, 620),
            (4, 460, 600)
            )
        for wall in self.map_data[self.checkpoint].get('data'):
            if wall[0] < 5:
                self.walls.add(Wall(self, wall))
        for wall in self.home:
            self.walls.add(Wall(self, wall))

    def init_map(self):
        for item in self.map_data[self.edit_checkpoint].get('data'):
            self.maps.add(Wall(self, item))

    def init_tank(self):
        self.tanks.add(Tank(400,600,self.player1,self))
        self.tanks.add(Tank(520,600,self.player2,self))

    def init_menu(self):
        for i in range(4):
            self.menus.add(Menu(i,362, 222 + 69 * i, self))
        self.menus.add(Menu(4, 820, 0, self))
        self.menus.add(Menu(5, 892, 0, self))

        pos = (610, 335), (709, 335), (610,378), (709, 378), (610, 421), (709, 421)
        for index, item in enumerate(pos):
            self.checkpoints.add(Checkpoint(index, item[0], item[1], self))

    def create_enemy_tank(self):
        if self.enemy_num > 0 and len(self.tanks) < self.enemy_show_num + 2:
            enemy_temp_tank = Tank(random.randrange(self.width - 39), 0 , self.enemy, self)
            collide_list = pygame.sprite.spritecollide(enemy_temp_tank, self.tanks, False, pygame.sprite.collide_mask)
            if not collide_list:
                self.tanks.add(enemy_temp_tank)
                self.enemy_num -= 1

    def edit_map(self):
        if len(self.maps) == 0:
            self.init_map()
        self.map.cursor()
        self.maps.draw(self.screen)

    def run(self, key, event):
        if self.is_music and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
        self.tanks.update(key,event)
        self.tanks.draw(self.screen)
        self.missiles.update()
        self.missiles.draw(self.screen)
        self.booms.update()
        self.booms.draw(self.screen)
        self.walls.draw(self.screen)
        self.rewards.update()
        self.rewards.draw(self.screen)
        self.joystick.update()

        enemy_now_num = self.enemy_num + len(self.tanks) - 2
        if enemy_now_num // 10 != 0:
            self.screen.blit(self.images.num.subsurface(enemy_now_num // 10 * 20, 0, 20, 17), (460, 2))
        self.screen.blit(self.images.num.subsurface(enemy_now_num % 10 * 20, 0 ,20, 17), (480, 2))

        self.screen.blit(self.images.player_empty, (5, self.height - 20))
        self.screen.blit(self.images.player_filled.subsurface(0, 0, 69 - 14 * (5 - self.player1_num), 13),#单个宽14，高13
            (5, self.height -20))#x=5 h=620 

        self.screen.blit(self.images.player_empty, (self.width - 74, self.height - 20))
        self.screen.blit(self.images.player_filled.subsurface(0, 0, 69 - 14 * (5 - self.player2_num), 13),
            (self.width - 74, self.height - 20))#x=886y=620

    def show_menu(self, event):
        self.screen.blit(self.images.menu_background, (0,0))
        if self.is_run:
            show_menu = 1, 3, 4, 5
        else:
            show_menu = 0, 2, 3, 4, 5
        self.menus.update(show_menu, event)
        self.menus.draw(self.screen)

    def show_checkpoint(self, event):
        self.screen.blit(self.images.checkpoint_background, (596, 320))
        self.checkpoints.update(event)
        self.checkpoints.draw(self.screen)

    def over(self):
        if self.is_mixer:
            self.music.over.play()
        pygame.mixer.music.stop()
        self.is_music = False
        self.is_mixer = False
        over_rect = self.images.over.get_rect()
        over_rect.center = self.width / 2 , self.height / 2
        self.screen.blit(self.images.over,over_rect)

    def win(self):
        if self.is_show_win:
            pygame.mixer.music.stop()
            self.is_show_win = False
            if self.is_mixer:
                self.music.win.play()
        elif self.step < 1500:
            self.screen.blit(self.images.checkpoint[self.checkpoint][0],(430,237))
            self.step -= 10

        elif self.step < 10:
            self.step = 4000
            self.is_win = False
            self.is_show_win = True
        else:
            win_rect = self.images.win.get_rect()
            win_rect.center = self.width / 2, self.height / 2
            self.screen.blit(self.images.win, win_rect)
            self.step -= 10

    def quit(self):
        pygame.quit()
        sys.exit()

    def running(self):
        while True:
            key_up_event = None
            mouse_event = None
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()


                    #手柄
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 1:
                        self.attack = 1
                        #print('button pressed',self.attack)
                if event.type == pygame.JOYBUTTONUP:
                    self.attack = 0
                if event.type == pygame.JOYHATMOTION:
                    if event.hat == 0:
                        if event.value == (1,0):
                            self.dx = 1
                        elif event.value == (-1,0):
                            self.dx = -1
                        elif event.value == (0,1):
                            self.dy = 1
                        elif event.value == (0,-1):
                            self.dy = -1
                        else:
                            self.dx = 0
                            self.dy = 0
                        #print('hat',self.dx,self.dy)
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis ==1:
                        if event.value >= 0.7:
                            self.dy = -1
                        elif event.value <= -0.7:
                            self.dy = 1
                        elif -0.7 < event.value < 0.7:
                            self.dy = 0
                        
                    if event.axis == 0:
                        if event.value >= 0.7:
                            self.dx = 1
                        elif event.value <= -0.7:
                            self.dx = -1
                        elif -0.7 < event.value < 0.7:
                            self.dx = 0



                elif event.type == KEYUP:
                    key_up_event = event
                elif event.type == KEYDOWN:
                    if self.is_run and event.key == K_ESCAPE:
                        self.is_show_menu = not self.is_show_menu
                elif event.type == MOUSEBUTTONDOWN and self.is_show_menu:
                    mouse_event = event
                if self.is_edit_map:
                    self.map.update(event)
            key = pygame.key.get_pressed()

            self.screen.blit(self.images.background,(0,0))

            if self.is_show_menu:
                self.show_menu(mouse_event)
            elif self.is_edit_map:
                self.edit_map()
            else:
                if self.is_over:
                    self.over()
                elif self.is_win:
                    self.win()
                else:
                    self.run(key, key_up_event)

            if self.is_show_checkpoint:
                self.show_checkpoint(mouse_event)

            if self.player1_num == 0 and self.player2_num == 0:
                self.is_over = True

            if self.enemy_num + len(self.tanks) -2 <= 0 and self.player1_num + self.player2_num > 0:
                if self.checkpoint < len(self.map_data) -1:
                    self.checkpoint += 1
                    self.step_reward = 6000
                else:
                    self.checkpoint = 0
                    self.difficult += 2
                self.is_win = True
                self.init()

            if self.is_win:
                self.win()

            if self.is_run and not self.is_show_menu:
                reward_temp = Reward(self)
                collide_list1 = pygame.sprite.spritecollide(reward_temp,self.walls,False,pygame.sprite.collide_mask)
                collide_list2 = pygame.sprite.spritecollide(reward_temp,self.rewards,False,pygame.sprite.collide_mask)
                if not collide_list1 and not collide_list2:
                    if self.step_reward < 0:
                        self.rewards.add(reward_temp)
                        self.step_reward = 6000
                        if self.is_mixer:
                            self.music.new_reward.play()
                else:
                    self.step_reward -= 1

            if self.select_rect is not None:
                pygame.draw.rect(self.screen,(255,255,255),self.select_rect, 1)

            self.create_enemy_tank()

            self.clock.tick(35)
            pygame.display.update()

game = TankGame()
game.running()

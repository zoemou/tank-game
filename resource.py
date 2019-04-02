import pygame

class Img(object):
    #图片资源

    def __init__(self):
        self.background = self.load('background') # 背景
        self.menu_background = self.load('menu_background') # 菜单背景
        self.checkpoint_background = self.load('checkpoint') #关卡
        self.super = self.load('super')
        self.blank = self.load('blank')
        self.num = self.load('num')
        self.win = self.load('win')
        self.player_empty = self.load('player_empty')
        self.player_filled = self.load('player_filled')
        self.over = self.load('over')
        self.icon = self.load('icon')
        self.missile = [  # 子弹
            self.images(self.load('bullet0')),
            self.images(self.load('bullet1')),
            self.images(self.load('bullet2')),
            self.images(self.load('bullet3'))
        ]
        self.tank = [  # 坦克
            self.images(self.load('tank0')),
            self.images(self.load('tank1')),
            self.images(self.load('tank2')),
            self.images(self.load('tank3'))
        ]
        self.wall = [  # 墙
            self.load('wall0'),
            self.load('wall1'),
            self.load('wall2'),
            self.load('wall3'),
            self.load('wall4'),
            self.load('wall5'),
        ]
        self.boom = [  # 坦克爆炸
            pygame.transform.scale(self.load('explode1'), (40, 40)),
            pygame.transform.scale(self.load('explode2'), (40, 40)),
            pygame.transform.scale(self.load('explode3'), (40, 40)),
            pygame.transform.scale(self.load('explode4'), (40, 40)),
            pygame.transform.scale(self.load('explode5'), (40, 40)),
            pygame.transform.scale(self.load('explode6'), (40, 40)),
            pygame.transform.scale(self.load('explode7'), (40, 40)),
            pygame.transform.scale(self.load('explode8'), (40, 40)),
            pygame.transform.scale(self.load('explode9'), (40, 40)),
        ]
        self.fire = [  # 发射子弹产生的小爆炸
            self.load('fire')
        ]
        self.menu = [  # 菜单
            [
                self.load('start'),
                self.load('start_hover'),
                self.load('start_lock')
            ],
            [
                self.load('not_pause'),
                self.load('not_pause_hover'),
                self.load('not_pause_lock')
            ],
            [
                self.load('edit_map'),
                self.load('edit_map_hover'),
                self.load('edit_map_lock')
            ],
            [
                self.load('quit'),
                self.load('quit_hover')
                # self.load('quit_lock')
            ],
            [
                self.load('mixer_on'),  # 音效开关
                self.load('mixer_off')
            ],
            [
                self.load('music_on'),  # 音乐开关
                self.load('music_off')
            ]
        ]
        self.checkpoint = [  # 关卡
            [
                self.load('checkpoint1'),
                self.load('checkpoint1_hover')
            ], [
                self.load('checkpoint2'),
                self.load('checkpoint2_hover')
            ], [
                self.load('checkpoint3'),
                self.load('checkpoint3_hover')
            ], [
                self.load('checkpoint4'),
                self.load('checkpoint4_hover')
            ], [
                self.load('checkpoint5'),
                self.load('checkpoint5_hover')
            ], [
                self.load('checkpoint6'),
                self.load('checkpoint6_hover')
            ],
        ]
        self.reward = [  # 随机物品
            self.load('health_kit'),
            self.load('box'),
            self.load('barrel'),
            self.load('reinforce')
        ]

    def load(self, name):
        # 图片统一载入方法
        return pygame.image.load('img/%s.png' % name).convert_alpha()


    def images(self, image):
        # 通过向上的坦克,转换出四个方向的坦克
        tank_images = {
            'up': image,
            'down': pygame.transform.flip(image, False, True),
            'left': pygame.transform.rotate(image, 90),
            'right': pygame.transform.rotate(image, 270),
        }
        return tank_images

class Music(object):
    def __init__(self):
        # 游戏胜利
        self.win = pygame.mixer.Sound('music/win.wav')
        # 发射子弹
        self.fire = pygame.mixer.Sound('music/fire.wav')
        # 设置发身子弹的音量
        self.fire.set_volume(0.5)
        # 游戏结束
        self.over = pygame.mixer.Sound('music/over.wav')
        # 坦克爆炸
        self.boom = pygame.mixer.Sound('music/boom.wav')
        self.boom.set_volume(0.5)
        # 出现随机物品
        self.new_reward = pygame.mixer.Sound('music/new_reward.wav')
        # 获得随机物品
        self.get_reward = pygame.mixer.Sound('music/get_reward.wav')
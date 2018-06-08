
import random
import pygame

# 定义常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
FPS = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 发射子弹时间
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprites(pygame.sprite.Sprite):
    """飞机大战游戏精灵"""

    def __init__(self, image_name, speed=1):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect  = self.image.get_rect()
        self.speed = speed

    def update(self):
        """在屏幕的垂直方向运动"""
        self.rect.y += self.speed


class Background(GameSprites):
    """游戏背景精灵"""
    def __init__(self, is_alt=False):
        # 1. 调用父类方法创建一个精灵对象
        super().__init__("./images/background.png")
        # 2. 判断是否是交替图像
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        # 1. 调用父类的方法实现
        super().update()
        # 2. 判断是否移除屏幕
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprites):
    """创建敌机类"""
    def __init__(self):
        # 1. 调用父类方法创建一个敌机对象
        super().__init__("./images/enemy1.png")
        # 指定随机速度： 1 ~ 3
        self.speed = random.randint(1, 3)
        self.rect.y = -self.rect.height
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)

    def update(self):

        # 1. 调用父类方法，保持垂直飞行
        super().update()
        # 2. 判断是否飞出屏幕，是 - 删除对象
        if self.rect.y > SCREEN_RECT.height:
            # print("飞出屏幕")
            # kill方法可以讲精灵从精灵组中删除，避免内存消耗
            self.kill()


class Hero(GameSprites):
    # 英雄类
    def __init__(self):
        # 1. 调用父类方法
        super().__init__("./images/me1.png", 0)
        # 2. 设置初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom  = SCREEN_RECT.bottom - 120
        self.speed_h = 0
        self.speed_v = 0
        # 3. 创建子弹精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):

        # 水平方向移动
        self.rect.x += self.speed_h
        # 竖直方向移动
        self.rect.y += self.speed_v
        # 控制英雄不能移出屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.bottom > SCREEN_RECT.height:
            self.rect.bottom = SCREEN_RECT.height

    def fire(self):
        # 发射子弹
        for i in range(3):
            # 1. 创建子弹精灵
            bullets = Bullet()
            # 2. 设置精灵位置
            bullets.rect.bottom = self.rect.y - i * 20
            bullets.rect.centerx = self.rect.centerx
            # 3. 将精灵添加到精灵组
            self.bullets.add(bullets)


class Bullet(GameSprites):
    # 子弹类
    def __init__(self):
        # 1. 调用父类方法
        super().__init__("./images/bullet1.png", -10)

    def update(self):
        super().update()
        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()

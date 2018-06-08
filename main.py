#
from plane_sprites import *


class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("游戏初始化.....")
        # 1. 创建游戏窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. 创建时钟对象
        self.fps = pygame.time.Clock()
        # 3. 调用私有方法、创建sprites
        self.__create_sprites()
        # 4. 设置定时器时间 - 创建敌机 1.0s
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        # 5. 设置定时器时间 - 创建子弹 0.5s
        pygame.time.set_timer(HERO_FIRE_EVENT, 200)

    def __create_sprites(self):
        """创建背景图像和精灵组"""
        # 创建背景图像
        bg1 = Background()
        bg2 = Background(1)
        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机的精灵组（不必添加精灵）
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄精灵
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def star_game(self):
        print("游戏开始......")
        while True:
            # 1. 设置刷新频率fps
            self.fps.tick(FPS)
            # 2. 监听事件
            self.__event_handler()
            # 3. 碰撞检测
            self.__check_collide()
            # 4. 更新、绘制sprites
            self.__update_sprites()
            # 5. 更新显示
            pygame.display.flip()

    def __event_handler(self):
        """时间监听"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over()

            elif event.type == CREATE_ENEMY_EVENT:
                # print("敌机出场...")
                enemy = Enemy()
                # 将敌机精灵添加到精灵组中
                self.enemy_group.add(enemy)

            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.speed_h = +10
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed_h = -10
        elif keys_pressed[pygame.K_UP]:
            self.hero.speed_v = -10
        elif keys_pressed[pygame.K_DOWN]:
            self.hero.speed_v = +10
        else:
            self.hero.speed_h = 0
            self.hero.speed_v = 0

    def __check_collide(self):
        """碰撞检测"""
        # 1. 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        # 2. 敌机撞击英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            self.hero.kill()
            print("英雄牺牲......")
            self.__game_over()

    def __update_sprites(self):
        """更新精灵组"""
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():
        """游戏结束,不使用属性，所以用@staticmethod"""
        print("-"*10, "游戏结束", "-"*10)
        pygame.quit()
        exit()


if __name__ == '__main__':

    # 创建游戏对象
    game = PlaneGame()
    # 启动游戏
    game.star_game()

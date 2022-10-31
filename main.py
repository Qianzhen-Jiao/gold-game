import random
import pygame
import time
import sys
import threading
from settings import Settings
from box import Box
from drop import Drop, Bomb
from scoreboard import Scoreboard

class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.bg_color = self.settings.bg_color
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        # self.background = pygame.image.load('images/bg.png').convert()

        pygame.display.set_caption("Gold Game")
        self.boxs = pygame.sprite.Group()
        self.drops = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.scoreboard = Scoreboard(self)
        th1 = threading.Thread(target=self.create_drops)
        th1.setDaemon(True)
        th1.start()
        th2 = threading.Thread(target=self.create_bombs)
        th2.setDaemon(True)
        th2.start()
        

    def run(self):
        self._new_box()
        while True:
            self._check_events() # 事件检查方法，用于监听鼠标和键盘事件
            self._update_box()
            self._update_drop()
            self._update_bomb()
            self._update_screen()# 调用刷新屏幕方法

    def regame(self):
        self.scoreboard.score = 0
        self.boxs.empty()
        self.drops.empty()
        self.bombs.empty()
        self.scoreboard.prep_score()
        self.run()

    def _check_events(self):
        # 事件检查方法
        for event in pygame.event.get():
            if event.type == pygame.QUIT:# 如果关闭游戏，程序结束
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:# 如果按下键盘，进行键盘判断
                self._check_keydown_event(event)
                    
            elif event.type == pygame.KEYUP:# 如果抬起键值，执行相应操作
                self._check_keyup_event(event)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:# 判断鼠标点击事件
                mouse_pos = pygame.mouse.get_pos() #得到鼠标点击的坐标
                pass


    def _check_keydown_event(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT: # 如果按下键盘右键，允许向右移动
            self.box.moving_right = True
        if event.key == pygame.K_LEFT:# 如果按下键盘左键，允许向左移动
            self.box.moving_left = True
        if event.key == pygame.K_q:# 如果按下q键，退出游戏
            sys.exit()
        if event.key == pygame.K_SPACE:# 如果按下空格，重置游戏
            self.regame()


    def _check_keyup_event(self, event):
    
        """按键取消"""
        if event.key == pygame.K_RIGHT:
            self.box.moving_right = False # 如果右键抬起，不允许移动
        if event.key == pygame.K_LEFT:
            self.box.moving_left = False # 如果左键抬起，不允许移动


    def _new_box(self):# 创建盒子对象
        self.box = Box(self)
        self.boxs.add(self.box)

    def _update_box(self):
        self.box.update()


    def create_drops(self):
        while True:
            self._new_drop()
            time.sleep(1.5)

            
    def _new_drop(self):
        new_drop = Drop(self)
        self.drops.add(new_drop)


    def _update_drop(self):
        self.drops.update()
        
        for drop in self.drops.copy():
            if drop.rect.bottom >= self.settings.screen_height:
                self.drops.remove(drop)
        self._check_boxs_drops_collisions()
    
    def _check_boxs_drops_collisions(self):
        collisions = pygame.sprite.groupcollide(self.boxs, self.drops, False, True)
        if collisions:
            for drops in collisions.values():
                self.scoreboard.score += len(drops)
            self.scoreboard.prep_score()

    def create_bombs(self):
        while True:
            self._new_bomb()
            print(random.randint(2,6))
            time.sleep(random.randint(2,6))

            
    def _new_bomb(self):
        new_bomb = Bomb(self)
        self.bombs.add(new_bomb)


    def _update_bomb(self):
        self.bombs.update()
        
        for bomb in self.bombs.copy():
            if bomb.rect.bottom >= self.settings.screen_height:
                self.bombs.remove(bomb)
        self._check_boxs_bombs_collisions()
    
    def _check_boxs_bombs_collisions(self):
        collisions = pygame.sprite.groupcollide(self.boxs, self.bombs, False, True)
        if collisions:
            for bombs in collisions.values():
                self.scoreboard.score -= len(bombs)
            self.scoreboard.prep_score()

    def _update_screen(self):# 屏幕刷新
        # self.screen.blit(self.background, (0, 0))
        self.screen.fill(self.settings.bg_color)# 填充颜色
        self.boxs.draw(self.screen)# 绘制盒子
        self.drops.draw(self.screen)# 绘制掉落物品
        self.bombs.draw(self.screen)# 绘制炸弹
        self.scoreboard.show_score()
        pygame.display.flip()# 刷新屏幕
        

if __name__ == "__main__":
    game = Game()
    game.run()

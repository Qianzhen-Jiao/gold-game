import pygame
from pygame.sprite import Sprite

class Box(Sprite):# 盒子类
    def __init__(self, game):
        super().__init__()# 编组初始化
        self.screen = game.screen
        self.settings = game.settings
        
        self.screen_rect = game.screen.get_rect() # 获得游戏界面的信息
        self.image = pygame.image.load("images/box.png")# 加载盒子图片
        self.rect = self.image.get_rect()# 获得图片的大小
        self.rect.center = self.screen_rect.center# 将图标设置在屏幕正中心
        self.rect.y = self.settings.screen_height - self.rect.height - 100 # 改变图标的y坐标
        self.x = float(self.rect.x)
        
        
        self.moving_right = False# 右移标志位
        self.moving_left = False# 左移标志位
        
    def update(self):# 更新盒子的位置
        # 右标志位为真并且没有超过界面边界
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.box_speed
        # 左标志位为真并且没有超过界面边界
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.box_speed
        self.rect.x = self.x
        

        

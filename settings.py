import pygame

class Settings:# 游戏设置类
    def __init__(self):
        self.screen_width = 800# 设置游戏的宽度
        self.screen_height = 700# 设置游戏的高度
        self.bg_color = (255, 255, 255)# 设置游戏的背景色
        # 设置四个按键的位置
        self.common_limit_time_button_coord = (self.screen_width//2, self.screen_height//4+60)
        self.common_nolimit_time_button_coord = (self.screen_width//2, self.screen_height//4+120)
        self.super_limit_time_button_coord = (self.screen_width//2, self.screen_height//4+180)
        self.super_nolimit_time_button_coord = (self.screen_width//2, self.screen_height//4+240)
        # 盒子移动速度
        self.box_speed = 1.2
        # 物品掉落速度
        self.drop_speed = 0.5
        
        
        

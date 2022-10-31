import pygame
import sys
import time
from settings import Settings
from box import Box
from drop import SmallGold, BigGold, Bomb, RedHeart, GoldStar, GrayStar, SmallLightning, BigLightning
from button import Model_common_limit_time, Model_common_nolimit_time, Model_super_limit_time, Model_super_nolimit_time
from states import GameStates
from scoreboard import Scoreboard
from clock import Clock
from life import Life
from countdown import Countdown



class GoldReceive:
    '''
    本类是游戏的顶层接口，所有其他类都要在本类中实例化并调用
    '''
    def __init__(self):
        pygame.init()# pygame初始化
        
        self.settings = Settings()# 导入游戏的设置类，Settings类在settings.py中
        self.bg_color = (230, 230, 230) # 设置游戏的背景颜色
        # 设置游戏框的宽度和高度
        self.screen = pygame.display.set_mode((self.settings.screen_width, 
                                               self.settings.screen_height)) 
        # 设置游戏框的名字
        pygame.display.set_caption("Receive Gold")
        
        # 以下几个都是实例化各种物品的编组，box类在box.py中，其他的类都在drop.py中
        self.boxs = pygame.sprite.Group()
        self.small_golds = pygame.sprite.Group()
        self.big_golds = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.red_hearts = pygame.sprite.Group()
        self.gold_stars = pygame.sprite.Group()
        self.gray_stars = pygame.sprite.Group()
        self.small_lightnings = pygame.sprite.Group()
        self.big_lightnings = pygame.sprite.Group()
        
        # 实例化四个按键的对象，四个类在button.py中
        self.common_limit_time_button = Model_common_limit_time(self, "限时间普通生命")
        self.common_nolimit_time_button = Model_common_nolimit_time(self, "不限时间普通生命")
        self.super_limit_time_button = Model_super_limit_time(self, "限时间超级模式")
        self.super_nolimit_time_button = Model_super_nolimit_time(self, "不限时间超级模式")
        
        # 实例化states类，类在states.py中
        self.states = GameStates(self)

        # 实例化三个成果类
        self.clock = Clock(self) # 类在clock.py中
        self.sb = Scoreboard(self)# 类在scoreboard.py中
        self.life = Life(self)# 类在life.py中
        
        # 实例化线程创建程序
        self.countdown = Countdown(self)# 类在countdown.py中
    def run_game(self):
        self._new_box() # 新建一个盒子对象

        while True:
            self._check_events() # 事件检查方法，用于监听鼠标和键盘事件
    
            if self.states.common_limit_time_active: # 判断是否属于限时间普通生命，为真则是
                self.box.update() # 更新盒子的位置
                self._update_bombs() # 更新炸弹的位置
                self._update_red_hearts() # 更新红心的位置
                self._update_small_golds() # 更新小金币的位置
                self._update_clock() # 更新时间成果
                if self.states.time == 0: # 如果时间为0，则说明游戏结束，重置游戏
                    self.states.reset_states()

            
            if self.states.common_nolimit_time_active:# 判断是否属于不限时间普通生命，为真则是
                self.box.update()
                self._update_bombs()
                self._update_small_golds()
                if self.states.vita == 0:
                    self.states.reset_states()
            
            if self.states.super_limit_time_active:# 判断是否属于限超级生命，为真则是
                self.box.update()
                self._update_bombs()
                self._update_red_hearts()
                self._update_small_golds()
                self._update_big_golds()
                self._update_gold_stars()
                self._update_gray_stars()
                self._update_big_lightnings()
                self._update_clock()
                if self.states.time == 0: 
                    self.states.reset_states()
                    time.sleep(1)
            
            if self.states.super_nolimit_time_active:# 判断是否属于不限时间超级生命，为真则是
                self.box.update()
                self._update_bombs()
                self._update_red_hearts()
                self._update_small_golds()
                self._update_big_golds()
                self._update_gold_stars()
                self._update_gray_stars()
                self._update_small_lightnings()
                if self.states.vita == 0:
                    self.states.reset_states()
            self._update_screen()# 调用刷新屏幕方法
            
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
                # 用于判断是否是按下按钮
                self._check_common_limit_time_button(mouse_pos)
                self._check_common_nolimit_time_button(mouse_pos)
                self._check_super_limit_time_button(mouse_pos)
                self._check_super_nolimit_time_button(mouse_pos)
                              
    def _check_keydown_event(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT: # 如果按下键盘右键，允许向右移动
            self.box.moving_right = True
        if event.key == pygame.K_LEFT:# 如果按下键盘左键，允许向左移动
            self.box.moving_left = True 
        if event.key == pygame.K_q:# 如果按下q键，退出游戏
            sys.exit()
        if event.key == pygame.K_SPACE:# 如果按下空格，重置游戏
            self.states.reset_states()
            
    def _check_keyup_event(self, event):
    
        """按键取消"""
        if event.key == pygame.K_RIGHT:
            self.box.moving_right = False # 如果右键抬起，不允许移动
        if event.key == pygame.K_LEFT:
            self.box.moving_left = False # 如果左键抬起，不允许移动
    
    def _check_common_limit_time_button(self, mouse_pos): # 不限时间普通生命模式处理
        button_clicked = self.common_limit_time_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.states.common_limit_time_active: 
            self.settings.initialize_dynamic_settings()# 初始化所有物品类
            self.states.reset_states()# 重置游戏
            
            self.states.common_limit_time_active = True # 将不限时间普通生命标志位设置为真
            self.countdown._threading_common_limit_time() # 创建线程
            self.states.score = '--' # 因为不涉及分数，分数清除
            self.sb.prep_score() # 刷新得分
            self.clock.prep_score() # 刷新时间
            self.life.prep_score()# 刷新生命值
            
            self.small_golds.empty()# 清空小金币编组
            self.bombs.empty()# 清空炸弹编组
            self.red_hearts.empty()# 清空红心编组
            
    # 以下三个方法都如同上一个方法，此处不再赘余
    def _check_common_nolimit_time_button(self, mouse_pos):
        button_clicked = self.common_nolimit_time_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.states.common_nolimit_time_active:
            self.settings.initialize_dynamic_settings()
            self.states.reset_states()
            
            self.states.common_nolimit_time_active = True
            self.countdown._threading_common_nolimit_time()
            self.states.time = '--'
            self.states.score = '--'
            self.sb.prep_score()
            self.clock.prep_score()
            self.life.prep_score()
            
            self.small_golds.empty()
            self.bombs.empty()

    def _check_super_limit_time_button(self, mouse_pos):
        button_clicked = self.super_limit_time_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.states.super_limit_time_active:
            self.settings.initialize_dynamic_settings()
            self.states.reset_states()
            
            self.states.super_limit_time_active = True
            self.countdown._threading_super_limit_time()
            self.sb.prep_score()
            self.clock.prep_score()
            self.life.prep_score()
            
            self.small_golds.empty()
            self.big_golds.empty()
            self.bombs.empty()
            self.gold_stars.empty()
            self.gray_stars.empty()
            self.red_hearts.empty()
            self.big_lightnings.empty()
   
    def _check_super_nolimit_time_button(self, mouse_pos):
        button_clicked = self.super_nolimit_time_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.states.super_nolimit_time_active:
            self.settings.initialize_dynamic_settings()
            self.states.reset_states()
            
            self.states.super_nolimit_time_active = True
            self.countdown._threading_super_nolimit_time()
            self.sb.prep_score()
            self.clock.prep_score()
            self.life.prep_score()
            
            self.small_golds.empty()
            self.big_golds.empty()
            self.bombs.empty()
            self.gold_stars.empty()
            self.gray_stars.empty()
            self.red_hearts.empty()
            self.small_lightnings.empty()

    
    def _new_box(self):# 创建盒子对象
        self.box = Box(self)
        self.boxs.add(self.box)

        
    def _new_small_gold(self):# 创建金币对象
        new_samll_gold = SmallGold(self)
        self.small_golds.add(new_samll_gold)
    
    def _update_small_golds(self):
        self.small_golds.update()
        # 刷新金币的位置
        for small_gold in self.small_golds.copy(): # 判断金币是否调出屏幕外，是则移除该金币，节约内存
            if small_gold.rect.bottom>=self.settings.screen_height:
                self.small_golds.remove(small_gold)
        self._check_boxs_small_golds_collisions()# 碰撞检测
    
    def _check_boxs_small_golds_collisions(self):
        collisions = pygame.sprite.groupcollide(self.boxs, self.small_golds, False, True)

        if collisions:# 如果金币和盒子发生碰撞，判断舒服哪个模式，并进行对向的成果变化
            if self.states.common_limit_time_active:
                for small_golds in  collisions.values():
                    self.states.vita += len(small_golds)
                self.life.prep_score()
            elif self.states.common_nolimit_time_active:
                for small_golds in  collisions.values():
                    self.states.vita += len(small_golds)
                if self.states.vita >= 20 : self.states.vita = 20
                self.life.prep_score()
            elif self.states.super_limit_time_active:
                for small_golds in collisions.values():
                    self.states.score += len(small_golds)
                self.sb.prep_score()
            elif self.states.super_nolimit_time_active:
                for small_golds in collisions.values():
                    self.states.score += len(small_golds)
                self.sb.prep_score()
            
    # 以下几个方法都与上面三个方法类似，此处不再赘余
    def _new_big_gold(self):
        new_big_gold = BigGold(self)
        self.big_golds.add(new_big_gold)
    
    def _update_big_golds(self):
        self.big_golds.update()
        
        for big_gold in self.big_golds.copy():
            if big_gold.rect.bottom>=self.settings.screen_height:
                self.big_golds.remove(big_gold)
        self._check_boxs_big_golds_collisions()
    
    def _check_boxs_big_golds_collisions(self):
        collisions = pygame.sprite.groupcollide(self.boxs, self.big_golds, False, True)

        if collisions:
            if self.states.super_limit_time_active:
                for big_golds in collisions.values():
                    self.states.score += 10 * len(big_golds)
                self.sb.prep_score()
            elif self.states.super_nolimit_time_active:
                for big_golds in collisions.values():
                    self.states.score += 10 * len(big_golds)
                self.sb.prep_score()


        
    def _new_bomb(self):
        new_bomb = Bomb(self)
        self.bombs.add(new_bomb)
        
    def _update_bombs(self):
        self.bombs.update()
        
        for bomb in self.bombs.copy():
            if bomb.rect.bottom>=self.settings.screen_height:
                self.bombs.remove(bomb)
        self._check_boxs_bombs_collisions()
        
    def _check_boxs_bombs_collisions(self):
        collisions = pygame.sprite.groupcollide(self.boxs, self.bombs, False, True)

        if collisions:
            if self.states.common_limit_time_active:
                for bombs in  collisions.values():
                    self.states.time -= len(bombs)
                self.clock.prep_score()
            elif self.states.common_nolimit_time_active:
                for bombs in  collisions.values():
                    self.states.vita -= len(bombs)
                self.life.prep_score()
            elif self.states.super_limit_time_active:
                for bombs in  collisions.values():
                    self.states.time -= len(bombs)
                self.clock.prep_score()
            elif self.states.super_nolimit_time_active:
                for bombs in  collisions.values():
                    self.states.vita -= len(bombs)
                self.life.prep_score()


                
    def _new_gold_star(self):
        new_gold_star = GoldStar(self)
        self.gold_stars.add(new_gold_star)
        
    def _update_gold_stars(self):
        self.gold_stars.update()
        
        for gold_star in self.gold_stars.copy():
            if gold_star.rect.bottom>=self.settings.screen_height:
                self.gold_stars.remove(gold_star)
        self._check_boxs_gold_stars_collisions()
    
    def _check_boxs_gold_stars_collisions(self):
        collisions = pygame.sprite.groupcollide(self.boxs, self.gold_stars, False, True)

        if collisions:
            if self.states.super_limit_time_active:
                for gold_stars in collisions.values():
                    self.settings.box_speed *= self.settings.box_speedup_scale * len(gold_stars)
            elif self.states.super_nolimit_time_active:
                for gold_stars in collisions.values():
                    self.settings.box_speed *= self.settings.box_speedup_scale * len(gold_stars)

                    
                    
    def _new_gray_star(self):
        new_gray_star = GrayStar(self)
        self.gray_stars.add(new_gray_star)

    def _update_gray_stars(self):
        self.gray_stars.update()
        
        for gray_star in self.gray_stars.copy():
            if gray_star.rect.bottom>=self.settings.screen_height:
                self.gray_stars.remove(gray_star)
        self._check_boxs_gray_stars_collisions()
    
    def _check_boxs_gray_stars_collisions(self):
        collisions = pygame.sprite.groupcollide(self.boxs, self.gray_stars, False, True)

        if collisions:
            if self.states.super_limit_time_active:
                for gray_stars in collisions.values():
                    self.settings.box_speed /= self.settings.box_speedup_scale * len(gray_stars)
            if self.states.super_nolimit_time_active:
                for gray_stars in collisions.values():
                    self.settings.box_speed /= self.settings.box_speedup_scale * len(gray_stars)
    
    
    def _new_red_heart(self):
        new_red_heart = RedHeart(self)
        self.red_hearts.add(new_red_heart)

    def _update_red_hearts(self):
        self.red_hearts.update()
        
        for red_heart in self.red_hearts.copy():
            if red_heart.rect.bottom>=self.settings.screen_height:
                self.red_hearts.remove(red_heart)
        self._check_boxs_red_hearts_collisions()
    
    def _check_boxs_red_hearts_collisions(self):
        collisions = pygame.sprite.groupcollide(self.boxs, self.red_hearts, False, True)
        if collisions:
            if self.states.common_limit_time_active:
                for red_hearts in collisions.values():
                    self.states.time += len(red_hearts)
                self.clock.prep_score()
            elif self.states.super_limit_time_active:
                for red_hearts in collisions.values():
                    self.states.time += len(red_hearts)
                self.clock.prep_score()
            elif self.states.super_nolimit_time_active:
                for red_hearts in collisions.values():
                    self.states.vita += len(red_hearts)
                self.life.prep_score()
    
    
    def _new_small_lightning(self):
        new_small_lightning = SmallLightning(self)
        self.small_lightnings.add(new_small_lightning)

    def _update_small_lightnings(self):
        self.small_lightnings.update()
        
        for small_lightning in self.small_lightnings.copy():
            if small_lightning.rect.bottom>=self.settings.screen_height:
                self.small_lightnings.remove(small_lightning)
        self._check_boxs_small_lightnings_collisions()
    
    def _check_boxs_small_lightnings_collisions(self):
        collisions = pygame.sprite.groupcollide(self.boxs, self.small_lightnings, False, True)

        if collisions:
            if self.states.super_nolimit_time_active:
                for small_lightnings in collisions.values():
                    pass
                self.sb.prep_score() 


    def _new_big_lightning(self):
        new_big_lightning = BigLightning(self)
        self.big_lightnings.add(new_big_lightning)

    def _update_big_lightnings(self):
        self.big_lightnings.update()
        
        for big_lightning in self.big_lightnings.copy():
            if big_lightning.rect.bottom>=self.settings.screen_height:
                self.big_lightnings.remove(big_lightning)
        self._check_boxs_big_lightnings_collisions()
    
    def _check_boxs_big_lightnings_collisions(self):
        collisions = pygame.sprite.groupcollide(self.boxs, self.big_lightnings, False, True)

        if collisions:
            if self.states.super_limit_time_active:
                for big_lightnings in collisions.values():
                    self.states.score *= 2 * len(big_lightnings)
                self.sb.prep_score()      


    # 刷新时间
    def _update_clock(self):
        self.clock.prep_score()
    
    def _update_screen(self):# 屏幕刷新
        self.screen.fill(self.settings.bg_color)# 填充颜色
        self.boxs.draw(self.screen)# 绘制盒子
        self.small_golds.draw(self.screen)# 绘制小金币
        self.big_golds.draw(self.screen)
        self.bombs.draw(self.screen)
        self.gold_stars.draw(self.screen)
        self.gray_stars.draw(self.screen)
        self.red_hearts.draw(self.screen)
        self.small_lightnings.draw(self.screen)
        self.big_lightnings.draw(self.screen)
        self.sb.show_score()# 绘制分数
        self.clock.show_time()
        self.life.show_vita()
        if not (self.states.common_limit_time_active or  
                self.states.common_nolimit_time_active or
                self.states.super_limit_time_active or
                self.states.super_nolimit_time_active):
                
            # 如果不处于游戏中，显示模式选择按键
            self.common_limit_time_button.draw_button()
            self.common_nolimit_time_button.draw_button()
            self.super_limit_time_button.draw_button()
            self.super_nolimit_time_button.draw_button()
        pygame.display.flip()# 刷新屏幕
            
if __name__ == "__main__":
    gold = GoldReceive()# 实例化接金币游戏
    gold.run_game()# 运行游戏
    
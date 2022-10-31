import pygame.font

# 本类的注释与life.py文件相同
class Scoreboard:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.score = 0
        
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 40)
        self.prep_score()
        self.scoreIcon = ScoreIcon(self)
        
    def prep_score(self):
        score_str = str(self.score)

        self.score_image = self.font.render(score_str, 
                                            True, 
                                            self.text_color, 
                                            self.settings.bg_color)
        
        # 在屏幕右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.scoreIcon.update()

        
class ScoreIcon():
    def __init__(self, Scoreboard):
        self.screen = Scoreboard.screen
        self.settings = Scoreboard.settings
        
        self.screen_rect = Scoreboard.screen.get_rect()
        self.score_rect = Scoreboard.score_rect
        self.image = pygame.image.load("images/{}.png".format('score'))
        self.rect = self.image.get_rect()

    def update(self):
    
        self.rect.center = self.score_rect.center
        self.rect.left = self.score_rect.left - 60
        self.screen.blit(self.image, self.rect)

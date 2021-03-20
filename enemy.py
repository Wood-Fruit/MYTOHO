import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):

    def __init__(self, ai_setting, screen, stats):
        # initialize enemy and square
        super(Enemy, self).__init__()
        self.screen = screen
        self.ai_setting = ai_setting

        # load the pic and set the rect
        self.image = pygame.image.load('images/little_enemy.png')
        self.rect = self.image.get_rect()

        # put at the center of bottom
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the accurate position
        self.x = float(self.rect.x)
        self.GameStats = stats

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        if self.ai_setting.fleet_direction < 0:
            self.image = pygame.image.load('images/little_enemy_reverse.png')
        else:
            self.image = pygame.image.load('images/little_enemy.png')
        self.x += ((self.ai_setting.enemy_speed_factor + self.GameStats.difficulty) *
                   self.ai_setting.fleet_direction)
        self.rect.x = self.x

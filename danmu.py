import pygame
from pygame.sprite import Sprite


class Danmu(Sprite):

    def __init__(self, ai_setting, screen, char):
        super(Danmu, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, ai_setting.danmu_width,
                                ai_setting.danmu_height)
        self.rect.centerx = char.rect.centerx
        self.rect.top = char.rect.top
        self.y = float(self.rect.y)
        self.color = ai_setting.danmu_color
        self.speed_factor = ai_setting.danmu_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_danmu(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

import pygame


class Char:

    def __init__(self, ai_setting, screen):
        # initialize character and square
        self.screen = screen
        self.image = pygame.image.load('images/char_low.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # put at the center of bottom
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.moving_slow = False
        self.shooting = False
        self.ai_setting = ai_setting
        self.center = float(self.rect.centerx)
        self.last_time_fired = 0
        self.bomb = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_slow:
            current_speed = self.ai_setting.char_speed_factor - self.ai_setting.slow
        else:
            current_speed = self.ai_setting.char_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += current_speed
            self.image = pygame.image.load('images/char_right.png')
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= current_speed
            self.image = pygame.image.load('images/char_left.png')
        if self.moving_up and self.rect.top > 0:
            self.rect.bottom -= current_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.bottom += current_speed
        if not self.moving_left and not self.moving_right:
            self.image = pygame.image.load('images/char_low.png')

    def center_char(self):
        """locate the char in the middle"""
        self.center = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

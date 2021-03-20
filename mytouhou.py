import pygame
from pygame.sprite import Group
from enemy import Enemy
from setting import Setting
from char import Char
import game_functions as gf
from GameStats import GameStats
from button import Button


def run_game():
    # initialize and create a screen
    pygame.init()
    ai_setting = Setting()
    screen = pygame.display.set_mode(
        (ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption('MY TOUHOU')
    play_button = Button(ai_setting, screen, 'Play')
    # add char danmu and enemy
    char = Char(ai_setting, screen)
    danmus = Group()
    stats = GameStats(ai_setting)
    enemy = Enemy(ai_setting, screen, stats)
    enemies = Group(enemy)
    gf.create_fleet(ai_setting, screen, char, enemies, stats)

    print('MYTOHO V0.1 ALL RIGHTS RESERVED')
    # main loop
    while True:
        # monitor key and mouse event
        gf.check_events(ai_setting, screen, stats, play_button, char, danmus)
        if stats.game_active:
            char.update()
            gf.update_danmu(ai_setting, screen, stats, char, enemies, danmus)
            gf.update_enemies(ai_setting, stats, screen, char, enemies, danmus)
        gf.update_screen(ai_setting, screen, stats, char, enemies, danmus, play_button)


run_game()

import sys
import time
from time import sleep
from danmu import Danmu
from enemy import Enemy
import pygame


def check_keydown_events(event, char):
    if event.key == pygame.K_RIGHT:
        # move right
        char.moving_right = True
    if event.key == pygame.K_LEFT:
        # move left
        char.moving_left = True
    if event.key == pygame.K_UP:
        # move right
        char.moving_up = True
    if event.key == pygame.K_DOWN:
        # move left
        char.moving_down = True
    if event.key == pygame.K_LSHIFT:
        char.moving_slow = True
    if event.key == pygame.K_z:
        char.shooting = True
    if event.key == pygame.K_x:
        char.bomb = True


def check_keyup_events(event, char):
    if event.key == pygame.K_RIGHT:
        # stop moving right
        char.moving_right = False
    if event.key == pygame.K_LEFT:
        # stop moving left
        char.moving_left = False
    if event.key == pygame.K_UP:
        # stop moving right
        char.moving_up = False
    if event.key == pygame.K_DOWN:
        # stop moving left
        char.moving_down = False
    if event.key == pygame.K_LSHIFT:
        char.moving_slow = False
    if event.key == pygame.K_z:
        char.shooting = False
    if event.key == pygame.K_x:
        char.bomb = False


def check_events(ai_setting, screen, stats, play_button, char, danmus):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, char)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, char)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, stats, play_button, mouse_x, mouse_y)
    if char.shooting:
        if time.time() - char.last_time_fired > ai_setting.rate_of_fire:
            new_danmu = Danmu(ai_setting, screen, char)
            danmus.add(new_danmu)
            char.last_time_fired = time.time()
    if char.bomb:
        if stats.bomb:
            ai_setting.danmu_width = 1600
            new_danmu = Danmu(ai_setting, screen, char)
            danmus.add(new_danmu)
            ai_setting.danmu_width = 20
            stats.bomb -= 1


def update_screen(ai_setting, screen, stats, char, enemies, danmus, play_button):
    screen.fill(ai_setting.bg_color)
    for danmus in danmus.sprites():
        danmus.draw_danmu()
    char.blitme()
    enemies.draw(screen)
    # visualize the screen
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_danmu(ai_setting, screen, stats, char, enemies, danmus):
    danmus.update()
    for danmu in danmus.copy():
        if danmu.rect.bottom <= 0:
            danmus.remove(danmu)
    if pygame.sprite.groupcollide(danmus, enemies, True, True):
        stats.score += 500
        print('enemy eliminated!\nscore +500')

    if len(enemies) == 0:
        danmus.empty()
        create_fleet(ai_setting, screen, char, enemies, stats)
        stats.difficulty += 1
        stats.bomb += 1
        stats.score += 5000
        print('+5000 score!\nHere comes another wave!\nDifficulty increased!\n')


def get_number_enemies_x(ai_setting, enemy_width):
    available_space_x = ai_setting.screen_width - 2 * enemy_width
    number_enemies_x = int(available_space_x / (2 * enemy_width))
    return number_enemies_x


def create_enemy(ai_setting, screen, enemies, stats, enemy_number, row_number):
    enemy = Enemy(ai_setting, screen, stats)
    enemy_width = enemy.rect.width
    enemy.x = enemy_width + 2 * enemy_width * enemy_number
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number
    enemies.add(enemy)


def create_fleet(ai_setting, screen, char, enemies, stats):
    enemy = Enemy(ai_setting, screen, stats)
    number_enemies_x = get_number_enemies_x(ai_setting, enemy.rect.width)
    number_rows = get_number_rows(ai_setting, char.rect.height, enemy.rect.height)

    for row_number in range(number_rows):
        for enemy_number in range(number_enemies_x):
            create_enemy(ai_setting, screen, enemies, stats, enemy_number, row_number)


def get_number_rows(ai_setting, char_height, enemy_height):
    avalable_space_y = (ai_setting.screen_height -
                        (3 * enemy_height) - char_height)
    number_rows = int(avalable_space_y / (2 * enemy_height))
    return number_rows


def update_enemies(ai_setting, stats, screen, char, enemies, danmus):
    check_fleet_edges(ai_setting, enemies, stats)
    enemies.update()
    check_aliens_bottom(ai_setting, stats, screen, char, enemies, danmus)

    if pygame.sprite.spritecollideany(char, enemies):
        char_hit(ai_setting, stats, screen, char, enemies, danmus)


def check_fleet_edges(ai_setting, enemies, stats):
    for enemy in enemies.sprites():
        if enemy.check_edges():
            change_fleet_direction(ai_setting, enemies, stats)
            break


def change_fleet_direction(ai_setting, enemies, stats):
    for enemy in enemies.sprites():
        enemy.rect.y += (ai_setting.fleet_drop_speed + stats.difficulty)
    ai_setting.fleet_direction *= -1


def char_hit(ai_setting, stats, screen, char, enemies, danmus):
    """react to the char hit by enemy"""
    if stats.char_left > 0:
        # char_1 minus 1
        stats.char_left -= 1

        # empty the list of enemies and bullets
        enemies.empty()
        danmus.empty()
        create_fleet(ai_setting, screen, char, enemies, stats)
        char.center_char()
        stats.score -= 500

        # pause
        sleep(0.5)
        print(
            'You lost a life! -500 scores!\nYou have ' + str(stats.char_left + 1) + ' lives left!\nyou survived ' + str(
                stats.difficulty) + ' waves!\ndifficulty restored!\n')
        stats.difficulty = 0
    else:
        stats.game_active = False
        stats.bomb = 0
        ai_setting.died = 1
        print('you died!\nyou survived ' + str(
            stats.difficulty) + ' waves!\n' + 'Score:' + str(
            stats.score) + '\nClick the play button to try again!\n')
        stats.score = 0


def check_aliens_bottom(ai_setting, stats, screen, char, enemies, danmus):
    screen_rect = screen.get_rect()
    for enemy in enemies.sprites():
        if enemy.rect.bottom >= screen_rect.bottom:
            char_hit(ai_setting, stats, screen, char, enemies, danmus)
            stats.score -= 100
            print('-100 scores!\nan enemy reached your base!\n')
            break


def check_play_button(ai_setting, stats, play_button, mouse_x, mouse_y):
    bonus = 0
    if stats.died:
        bonus = 1
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True
        stats.char_left = ai_setting.char_limit + bonus
        print('Game start, have fun!\n')
        stats.difficulty = 0

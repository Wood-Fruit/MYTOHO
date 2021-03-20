# store all of the settings
class Setting:

    # initialize the setting
    def __init__(self):
        # screen setting
        self.screen_width = 800
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.char_speed_factor = 5
        self.slow = 2
        self.danmu_speed_factor = 7
        self.danmu_width = 20
        self.danmu_height = 50
        self.danmu_color = (235, 200, 200)
        self.rate_of_fire = 0.5
        self.enemy_speed_factor = 1.5
        self.fleet_drop_speed = 30
        self.fleet_direction = 1
        self.char_limit = 2

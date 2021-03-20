class GameStats:
    def __init__(self, ai_setting):
        """initialize status system"""
        self.ai_setting = ai_setting
        self.reset_stats()
        self.game_active = False
        self.died = 0
        self.difficulty = 0
        self.bomb = 0
        self.score = 0

    def reset_stats(self):
        """initialize anything that could change during game"""
        self.char_left = self.ai_setting.char_limit
        self.difficulty = 0
        self.bomb = 0
        self.score = 0
        self.died = 0

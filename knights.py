import dice
import random


class knight:
    def __init__(self, name):
        self.hp = 3
        self.xp = 0
        self.name = name
        self.colors = []
        if self.name:
            if self.name = "Aziza":
                self.colors.append["black"]
                self.colors.append["brown"]
            elif self.name = "Black Angus":
                self.colors.append["black"]
            elif self.name = "Bombinus":
                self.colors.append["black"]
                self.colors.append["yellow"]
            elif self.name = "Brownie":
                self.colors.append["brown"]
            elif self.name = "Changeling":
                self.colors.append["pink"]
                self.colors.append["purple"]
            elif self.name = "Elfling":
                self.colors.append["brown"]
                self.colors.append["purple"]
            elif self.name = "Fjolla":
                self.colors.append["blue"]
                self.colors.append["white"]
            elif self.name = "Gloam Rider":
                self.colors.append["black"]
                self.colors.append["purple"]
            elif self.name = "Glory":
                self.colors.append["green"]
            elif self.name = "Gruagach":
                self.colors.append["purple"]
                self.colors.append["red"]
            elif self.name = "Kitsune":
                self.colors.append["blue"]
                self.colors.append["red"]
            elif self.name = "Leprechan":
                self.colors.append["green"]
            elif self.name = "Menehune":
                self.colors.append["brown"]
                self.colors.append["red"]
            elif self.name = "Naia":
                self.colors.append["green"]
                self.colors.append["yellow"]
            elif self.name = "Peri":
                self.colors.append["pink"]
                self.colors.append["yellow"]
            elif self.name = "Sugarplum":
                self.colors.append["blue"]
                self.colors.append["pink"]
            elif self.name = "The Godmother":
                self.colors.append["blue"]
            elif self.name = "Tinkerbelle":
                self.colors.append["brown"]
                self.colors.append["pink"]
            elif self.name = "Tooth Collector":
                self.colors.append["green"]
                self.colors.append["pink"]
            elif self.name = "Will o' the Wisp":
                self.colors.append["red"]
                self.colors.append["white"]
        self.populate_dice()


    def populate_dice(self):
        self.dice = []
        for color in self.colors:
            self.dice.append(die(color))


class die:
    def __init__(self, color):
        self.size = 6
        self.rerolls = 0
        self.min = 1
        self.bonus = 0
        self.color = color

    def roll(self):
        dice.roll(f"1d{self.size}r{self.min}+{self.bonus}")


class monster:
    def __init__(self, difficulty, game_rules):
        self.hp = 1
        self.difficulty = difficulty
        self.ranks = []
        for color in game_rules:
            self.ranks.append(color, 2)
        for i in range(0, difficulty + 1):
            random_rank = random.choice(self.ranks)
            random_rank[1] += 1


class game_rules:
    
    def __init__(self, party):
        # unselected colors will not be in the game
        colors = []
        for knight in party:
            for color in knight.colors:
                if color not in colors:
                    colors.append(color)



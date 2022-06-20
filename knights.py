import dice
import random


class knight:
    def __init__(self, name):
        self.hp = 3
        self.xp = 0
        self.name = name
        self.colors = []
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
        self.knights = {}
        self.name["Aziza"] = ["black", "brown"]
        self.name["Black Angus"] = ["black"]
        self.name["Bombinus"] = ["black", "yellow"]
        self.name["Brownie"] = ["brown"]
        self.name["Changeling"] = ["pink", "purple"]
        self.name["Elfling"] = ["brown", " purple"]
        self.name["Fjolla"] = ["blue", "white"]
        self.name["Gloam Rider"] = ["black", "purple"]
        self.name["Glory"] = ["green"]
        self.name["Gruagach"] = ["purple", "red"]
        self.name["Kitsune"] = ["blue", "red"]
        self.name["Leprechan"] = ["green"]
        self.name["Menehune"] = ["brown", "red"]
        self.name["Naia"] = ["green", "yellow"]
        self.name["Peri"] = ["pink", "yellow"]
        self.name["Sugarplum"] = ["blue", "pink"]
        self.name["The Godmother"] = ["blue"]
        self.name["Tinkerbelle"] = ["brown", "pink"]
        self.name["Tooth Collector"] = ["green", "pink"]
        self.name["Will o' the Wisp"] = ["red", "white"]

    def set_colors(self):
        self.colors = []
        for knight in party:
            for color in knight.colors:
                if color not in self.colors:
                    self.colors.append(color)

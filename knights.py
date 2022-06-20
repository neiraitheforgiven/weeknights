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
        self.splodey = 0
        self.count = 1
        self.color = color

    def roll(self):
        dice.roll(
            f"{self.count}d{self.size}r{self.min}x{self.size - self.splodey}^1+{self.bonus}t"
        )


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
    def __init__(self):
        self.colors = []
        self.knights = {}
        self.knights["Aziza"] = ["black", "brown"]
        self.knights["Black Angus"] = ["black"]
        self.knights["Bombinus"] = ["black", "yellow"]
        self.knights["Brownie"] = ["brown"]
        self.knights["Changeling"] = ["pink", "purple"]
        self.knights["Elfling"] = ["brown", " purple"]
        self.knights["Fjolla"] = ["blue", "white"]
        self.knights["Gloam Rider"] = ["black", "purple"]
        self.knights["Glory"] = ["green"]
        self.knights["Gruagach"] = ["purple", "red"]
        self.knights["Kitsune"] = ["blue", "red"]
        self.knights["Leprechan"] = ["green"]
        self.knights["Menehune"] = ["brown", "red"]
        self.knights["Naia"] = ["green", "yellow"]
        self.knights["Peri"] = ["pink", "yellow"]
        self.knights["Sugarplum"] = ["blue", "pink"]
        self.knights["The Godmother"] = ["blue"]
        self.knights["Tinkerbelle"] = ["brown", "pink"]
        self.knights["Tooth Collector"] = ["green", "pink"]
        self.knights["Will o' the Wisp"] = ["red", "white"]

    def set_colors(self, party):
        # unselected colors will not be in the game
        for knight in party:
            for color in knight.colors:
                if color not in self.colors:
                    self.colors.append(color)


class game:
    def __init__():
        party = []
        self.game_rules = game_rules()
        for i in range(4):
            knights = [
                knight.key() for knight in game_rules.knights if knight not in party
            ]
            options = random.sample(knights, 3)
            for option in options:
                i = option.index
                print(f"({i}) {option}, {game_rules.knights[option]}")
            choice = ""
            while choice not in ("1", "2", "3", "4", "q", "Q"):
                choice = input("Choose a knight or press (Q) to quit!")
            if choice in ("q", "Q"):
                exit()
            else:
                choice = int(choice)
                chosen_knight = options[choice]
                party.append(knight(game_rules.knights[chosen_knight]))

import dice
import random


class knight:
    def __init__(self, name, colors):
        self.hp = 3
        self.xp = 0
        self.name = name
        self.colors = colors
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
        self.knights["Glory"] = ["white", "yellow"]
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
        self.tiles = {}
        self.tiles["shop"] = 8
        self.tiles["camp"] = 12
        self.tiles["quest"] = 12
        self.tiles["elite"] = 10
        self.tiles["combat"] = 53

    def set_colors(self, party):
        # unselected colors will not be in the game
        for knight in party:
            for color in knight.colors:
                if color not in self.colors:
                    self.colors.append(color)


class map:
    """Heavily borrowed from aztuk's reverse engineered Slay the Spire map generator"""

    def __init__(self, game_rules, depth=7):
        self.game_rules = game_rules
        self.rings = []
        self.depth = depth
        for i in range(self.depth):
            rooms = list()
            for j in range((i + 1) * 8):
                print(f"appending {j} to {i}")
                rooms.append(None)
            self.rings.append(rooms)
        self.generate_path(0)
        self.generate_path(2)
        self.generate_path(4)
        self.generate_path(6)
        for ring in self.rings:
            print([room.type if room is not None else None for room in ring])

    def generate_path(self, first_room):
        current_room = room()
        combat_unlocked = True
        self.rings[0][first_room] = room()
        self.rings[0][first_room].type = "combat"
        remembered_room = first_room
        ring = 1
        while ring < self.depth - 1:
            parent_room = None
            random_room = self.get_random_cell_of_ring(
                self.rings[ring], remembered_room
            )
            if self.rings[ring][random_room]:
                parent_room = self.rings[ring][random_room]
            else:
                parent_room = room()
            self.rings[ring][random_room] = parent_room

            if not current_room in parent_room.child_rooms:
                parent_room.child_rooms.append(current_room)

            if not parent_room in current_room.parent_rooms:
                current_room.parent_rooms.append(parent_room)

            current_room = parent_room
            remembered_room = random_room

            ring += 1

    def get_random_cell_of_ring(self, ring, connection_room=None):
        lower_limit = 0
        upper_limit = len(ring) - 1
        if connection_room:
            lower_limit = max(connection_room - 1, lower_limit)
            upper_limit = min(connection_room + 1, upper_limit)
        room = random.randint(lower_limit, upper_limit)
        return room


class room:
    def __init__(self):
        self.type = None
        self.child_rooms = []
        self.parent_rooms = []


class game:
    def __init__(self):
        self.party = []
        self.game_rules = game_rules()
        for i in range(4):
            knights = [
                knight
                for knight in self.game_rules.knights
                if knight not in (party_member.name for party_member in self.party)
            ]
            options = random.sample(knights, 3)
            for i, option in enumerate(options):
                print(f"({i}) {option}, {self.game_rules.knights[option]}")
            choice = ""
            while choice not in ("1", "2", "3", "q", "Q"):
                choice = input("Choose a knight or press (Q) to quit: ")
            if choice in ("q", "Q"):
                exit()
            else:
                choice = int(choice) - 1
                chosen_knight = options[choice]
                self.party.append(
                    knight(chosen_knight, self.game_rules.knights[chosen_knight])
                )
        self.game_rules.set_colors(self.party)
        print("Party:")
        print(f"{[party_member.name for party_member in self.party]}")
        print("Colors:")
        print(f"{self.game_rules.colors}")
        self.map = map(self.game_rules)


game()

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
        for i in range(self.depth + 1):
            rooms = list()
            for j in range((i + 1) * 8):
                rooms.append(None)
            self.rings.append(rooms)
        self.generate_paths([1, 3, 5, 7])
        self.apply_types()
        self.make_sibling_connections()
        for ring in self.rings:
            print(
                [room.type or "untyped" if room is not None else None for room in ring]
            )
        self.draw_map(self.depth)

    def apply_types(self):
        for i, ring in enumerate(self.rings):
            rooms = [room for room in ring if room]
            for room in rooms:
                if not room.type:
                    room.set_type_from_rules(i, self.game_rules)

    def draw_map(self, depth):
        # draw map with no gapping first
        drawing = []
        # first create a blank set with no gaps
        for i in range(depth):
            drawing.append([None for x in range(depth)])
        # that should give you a 'square' of Nones. Now...
        for i, ring in reversed(list(enumerate(self.rings))):
            current_cell_from_start = 0
            current_cell_from_end = len(ring) - 1
            # get the first drawing row that contains ONLY Nones
            rows_with_empty = [
                row for row in drawing if not any([cell for cell in row if cell])
            ]
            straight_row = next(row for row in rows_with_empty)
            reverse_row = next(reversed([row for row in rows_with_empty]))
            the_rest_of_the_rows = [
                row for row in rows_with_empty if row not in (straight_row, reverse_row)
            ]
            for cid, cell in enumerate(straight_row):
                straight_row[cid] = ring[current_cell_from_start]
                current_cell_from_start += 1
            for row in the_rest_of_the_rows:
                first_cell = next([row.index(cell) for cell in row if not cell])
                last_cell = next(
                    reversed([row.index(cell) for cell in row if not cell])
                )
                row[last_cell] = ring[current_cell_from_start]
                current_cell_from_start += 1
                row[first_cell] = ring[current_cell_from_end]
                current_cell_from_start -= 1
            for cid, cell in enumerate(reverse_row):
                reverse_row[cid] = ring[current_cell_from_end]
                current_cell_from_start -= 1
            print(f"ring {i} processed")
        # now add a horizontal gap between each of the elements in each row
        drawing_with_gaps = []
        for row in drawing:
            gapped_row = []
            for cell in row:
                gapped_row.append(cell)
                gapped_row.append(map_room("hgap"))
            # remove the last gap
            gapped_row.pop()
            drawing_with_gaps.append(gapped_row)
            gap_row = []
            for i in range(depth):
                gap_row.append(map_room("vgap"))
                gap_row.append(map_room("xgap"))
            gap_row.pop()
            drawing_with_gaps.append(gap_row)
        drawing_with_gaps.pop()
        # if I did that right, I should get all the squares:
        for row in drawing_with_gaps:
            row_print = []
            for cell in row:
                if isinstance(cell, str):
                    row_print.append(cell)
                elif isinstance(cell, map_room):
                    row_print.append(cell.type or "untyped")
                else:
                    row_print.append(None)
            print(row_print)

    def generate_paths(self, first_room_seeds):
        # combat_unlocked = True
        for room in first_room_seeds:
            self.rings[0][room] = map_room()
            self.rings[0][room].type = "combat"
            self.rings[0][room].owed_paths += 1
        for ring in range(self.depth):
            # get all the rooms on this floor
            rooms = [room for room in self.rings[ring] if room]
            # get four random rooms on this floor and increment their owed_paths by 1
            splitting_rooms = random.sample(rooms, 4)
            for splitting_room in splitting_rooms:
                splitting_room.owed_paths += 1
            # iterate through all rooms and connect them
            target_ring = ring + 1
            for source_room in rooms:
                for connection in range(source_room.owed_paths):
                    target_room = None
                    random_room_id = self.get_random_cell_of_ring(
                        self.rings[target_ring], self.rings[ring].index(source_room)
                    )
                    # if this room is already populated, don't change it
                    if not self.rings[target_ring][random_room_id]:
                        self.rings[target_ring][random_room_id] = map_room()
                    target_room = self.rings[target_ring][random_room_id]

                    if target_room not in source_room.child_rooms:
                        source_room.child_rooms.append(target_room)

                    if source_room not in target_room.parent_rooms:
                        target_room.parent_rooms.append(source_room)

                    target_room.owed_paths += 1

    def get_random_cell_of_ring(self, ring, connection_room=None):
        lower_limit = 0
        upper_limit = len(ring) - 1
        if connection_room:
            lower_limit = max(connection_room - 1, lower_limit)
            upper_limit = min(connection_room + 1, upper_limit)
        room = random.randint(lower_limit, upper_limit)
        return room

    def make_sibling_connections(self):
        for ring in self.rings:
            rooms = [room for room in ring if room]
            for room in rooms:
                next_room, distance = room.get_next_room(ring)
                if next_room and distance:
                    if room.type == "combat" or room.type == next_room.type:
                        proceed = random.choice(range(distance))
                        if proceed == 0:
                            room.sibling_connection = next_room


class map_room:
    def __init__(self):
        self.type = None
        self.child_rooms = []
        self.parent_rooms = []
        self.owed_paths = 0
        self.sibling_connection = None

    def get_next_room(self, ring):
        my_num = ring.index(self)
        higher_rooms = [
            ring.index(room) for room in ring if room and ring.index(room) > my_num
        ]
        if higher_rooms:
            next_room = ring[min(higher_rooms)]
            distance = ring.index(next_room) - my_num
        if not higher_rooms:
            all_rooms = [ring.index(room) for room in ring if room]
            next_room = ring[min(all_rooms)]
            distance = len(ring) - my_num + ring.index(next_room)
        if distance:
            return next_room, distance

    def set_type_from_rules(self, ring, game_rules):
        tiles = [tile for tile in game_rules.tiles]
        weights = [game_rules.tiles[tile] for tile in game_rules.tiles]
        picked_types = random.choices(tiles, weights, k=1)
        picked_type = picked_types[0]
        if picked_type != "combat":
            for parent in self.parent_rooms:
                if parent.type == picked_type:
                    self.set_type_from_rules(ring, game_rules)
                    return
        if ring < 2 and picked_type == "shop":
            self.set_type_from_rules(ring, game_rules)
            return
        if ring < 4 and picked_type in ("camp", "elite"):
            self.set_type_from_rules(ring, game_rules)
            return
        self.type = picked_type


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

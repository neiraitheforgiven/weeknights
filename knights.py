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
                rooms.append(None)
            self.rings.append(rooms)
        self.generate_paths([1, 3, 5, 7])
        self.apply_types()
        self.make_sibling_connections()
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
        size = (2 * depth) + 1
        for i in range(size):
            drawing.append([None for x in range(size)])
        # that should give you a 'square' of Nones. Now...
        for i, ring in reversed(list(enumerate(self.rings))):
            print(f"ring {i}: {ring}")
            offset = depth - (i + 1)
            backset = (len(drawing) - 1) - offset
            current_cell_from_start = 0
            # get the first drawing row that contains ONLY Nones
            straight_row = drawing[offset]
            reverse_row = drawing[backset]
            the_rest_of_the_rows = drawing[offset + 1 : backset]
            for cid, cell in enumerate(straight_row):
                if offset <= cid <= backset:
                    drawing[offset][cid] = ring[current_cell_from_start]
                    current_cell_from_start += 1
            for rid, row in enumerate(the_rest_of_the_rows):
                cell = backset
                drawing[rid + offset + 1][cell] = ring[current_cell_from_start]
                current_cell_from_start += 1
            for cid, cell in reversed(list(enumerate(reverse_row))):
                if offset <= cid <= backset:
                    drawing[(backset) - offset][cid] = ring[current_cell_from_start]
                    current_cell_from_start += 1
            for rid, row in reversed(list(enumerate(the_rest_of_the_rows))):
                cell = offset
                drawing[rid + offset + 1][cell] = ring[current_cell_from_start]
                current_cell_from_start += 1
        # there will be a central tile that should become the palace
        drawing[depth + 1][depth + 1] = map_room("palace")
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
            for i in range(size):
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
        # now go through every tile and give it x, y coordinates
        # if the tile type is None, replace it with a tile of type 'void'
        for y, row in enumerate(drawing_with_gaps):
            for x, cell in enumerate(row):
                if cell:
                    if not cell.type:
                        cell.type = "void"
                else:
                    drawing_with_gaps[y][x] = map_room("void")
                    cell = drawing_with_gaps[y][x]
                cell.x = x
                cell.y = y
        for row in drawing_with_gaps:
            for cell in row:
                if cell and "gap" not in cell.type and "void" not in cell.type:
                    print(f"cell {cell.type} at {cell.x}, {cell.y}:")
                    print("  child_rooms:")
                    print(f"    {[concell.type for concell in cell.child_rooms]}")
                    print(f"    {[concell.x for concell in cell.child_rooms]}")
                    print(f"    {[concell.y for concell in cell.child_rooms]}")
                    print("  parent_rooms:")
                    print(f"    {[concell.type for concell in cell.parent_rooms]}")
                    print(f"    {[concell.x for concell in cell.parent_rooms]}")
                    print(f"    {[concell.y for concell in cell.parent_rooms]}")
                    if cell.sibling_connection:
                        print("  sibling_connection:")
                        print(
                            f"{cell.sibling_connection.type} {cell.sibling_connection.x}, {cell.sibling_connection.y}"
                        )
        # now, draw paths for all of the kinds of gaps
        for y, row in enumerate(drawing_with_gaps):
            for x, cell in enumerate(row):
                if cell.type == "hgap":
                    left_cell, right_cell = self.get_left_and_right_cells(
                        drawing_with_gaps, cell
                    )
                    if left_cell and right_cell:
                        if (
                            (
                                right_cell.child_rooms
                                and left_cell in right_cell.child_rooms
                            )
                            or (
                                right_cell.parent_rooms
                                and left_cell in right_cell.parent_rooms
                            )
                            or (left_cell.sibling_connection == right_cell)
                            or (right_cell.sibling_connection == left_cell)
                        ):
                            cell.type = "hpath"
                elif cell.type == "vgap":
                    up_cell, down_cell = self.get_up_and_down_cells(
                        drawing_with_gaps, cell
                    )
                    if up_cell and down_cell:
                        if (
                            (up_cell.child_rooms and down_cell in up_cell.child_rooms)
                            or (
                                up_cell.parent_rooms
                                and down_cell in up_cell.parent_rooms
                            )
                            or (down_cell.sibling_connection == up_cell)
                            or (up_cell.sibling_connection == down_cell)
                        ):
                            cell.type = "vpath"
                elif cell.type == "xgap":
                    (
                        left_up_cell,
                        right_down_cell,
                        left_down_cell,
                        right_up_cell,
                    ) = self.get_corner_cells(drawing_with_gaps, cell)
                    ascend = False
                    descend = False
                    if (
                        left_up_cell.child_rooms
                        and right_down_cell in left_up_cell.child_rooms
                    ) or (
                        left_up_cell.parent_rooms
                        and right_down_cell in left_up_cell.parent_rooms
                    ):
                        ascend = True
                    if (
                        left_down_cell.child_rooms
                        and right_up_cell in left_down_cell.child_rooms
                    ) or (
                        left_down_cell.parent_rooms
                        and right_up_cell in left_down_cell.parent_rooms
                    ):
                        descend = True
                    if ascend and descend:
                        cell.type = "xpath"
                    else:
                        if ascend:
                            cell.type = "ascpath"
                        elif descend:
                            cell.type = "descpath"
        self.pretty_print_drawing(drawing_with_gaps)

    def generate_paths(self, first_room_seeds):
        # combat_unlocked = True
        for room in first_room_seeds:
            self.rings[0][room] = map_room("combat", room)
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
            if target_ring < self.depth:
                for i, source_room in enumerate(rooms):
                    for connection in range(source_room.owed_paths):
                        target_room = None
                        index_with_offset = (source_room.source_id * (ring + 2)) + (
                            (source_room.offset_from_source * ring)
                        )
                        random_room_id = self.get_random_cell_of_ring(
                            self.rings[target_ring], index_with_offset
                        )
                        # if this room is already populated, don't change it
                        if not self.rings[target_ring][random_room_id]:
                            self.rings[target_ring][random_room_id] = map_room()
                        target_room = self.rings[target_ring][random_room_id]
                        target_room.source_id = source_room.source_id
                        target_room.offset_from_source = (
                            random_room_id - index_with_offset
                        )
                        if target_room not in source_room.child_rooms:
                            source_room.child_rooms.append(target_room)
                        if source_room not in target_room.parent_rooms:
                            target_room.parent_rooms.append(source_room)
                        target_room.owed_paths += 1

    def get_corner_cells(self, drawing, cell):
        source_x = cell.x
        source_y = cell.y
        if source_x in (0, len(drawing) - 1) or source_y in (0, len(drawing) - 1):
            return
        else:
            left_up_cell = drawing[source_y - 1][source_x - 1]
            left_down_cell = drawing[source_y + 1][source_x - 1]
            right_up_cell = drawing[source_y - 1][source_x + 1]
            right_down_cell = drawing[source_y + 1][source_x + 1]
        return left_up_cell, right_down_cell, left_down_cell, right_up_cell

    def get_left_and_right_cells(self, drawing, cell):
        source_x = cell.x
        source_y = cell.y
        if source_x in (0, len(drawing) - 1):
            return
        else:
            left_cell = drawing[source_y][source_x - 1]
            right_cell = drawing[source_y][source_x + 1]
            return left_cell, right_cell

    def get_up_and_down_cells(self, drawing, cell):
        source_x = cell.x
        source_y = cell.y
        if source_y in (0, len(drawing) - 1):
            return
        else:
            up_cell = drawing[source_y - 1][source_x]
            down_cell = drawing[source_y + 1][source_x]
            return down_cell, up_cell

    def get_random_cell_of_ring(self, ring, connection_room_index):
        lower_limit = 0
        upper_limit = len(ring) - 1
        if connection_room_index:
            lower_limit = max(connection_room_index - 1, lower_limit)
            upper_limit = min(connection_room_index + 1, upper_limit)
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

    def pretty_print_drawing(self, drawing):
        print("pretty_printing!")
        for row in drawing:
            print_row = ""
            for cell in row:
                if not cell:
                    print_row += " "
                elif cell.type in ("vgap", "hgap", "xgap", "void"):
                    print_row += " "
                elif cell.type == "elite":
                    print_row += "E"
                elif cell.type == "combat":
                    print_row += "c"
                elif cell.type == "shop":
                    print_row += "$"
                elif cell.type == "quest":
                    print_row += "?"
                elif cell.type == "hpath":
                    print_row += "-"
                elif cell.type == "vpath":
                    print_row += "|"
                elif cell.type == "ascpath":
                    print_row += "\\"
                elif cell.type == "descpath":
                    print_row += "/"
                elif cell.type == "xpath":
                    print_row += "X"
                elif cell.type == "camp":
                    print_row += "r"
                elif cell.type == "palace":
                    print_row += "P"
            print(print_row)


class map_room:
    def __init__(self, map_type=None, source_id=None):
        self.type = map_type
        self.child_rooms = []
        self.parent_rooms = []
        self.owed_paths = 0
        self.sibling_connection = None
        self.source_id = source_id
        self.offset_from_source = 0
        self.x = None
        self.y = None

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

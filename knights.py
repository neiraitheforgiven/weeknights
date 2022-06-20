import dice

class knight():

	def __init__(self):
		self.hp = 3
		self.xp = 0
		self.colors = []
		self.name = ""
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

class monster():
	
	def __init__(self):


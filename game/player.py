class Player:
    def __init__(self, name):
        self.name = name
        self.set_position(4) # atlanta
        self.cards = []
        self.action = 0

    def set_role(self, r):
        self.role = r

    def set_position(self, id):
        self.pos = id

    def add_picked(self, card):
        self.cards.append(card)

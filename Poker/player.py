class Player():
    def __init__(self, name, balance, hand, folded):
        self.name = name
        self.balance = balance
        self.hand = hand
        self.folded = folded

    def getBalance(self):
        return self.balance

    def addBalance(self, amount):
        self.balance += amount

    def reduceBalance(self, amount):
        self.balance -= amount

    def add_card(self, card):
        self.hand.append(card)

    def reset_hand(self):
        self.hand = []

    def fold(self):
        self.folded = True

    def unfold(self):
        self.folded = False

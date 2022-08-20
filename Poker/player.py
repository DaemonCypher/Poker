class Player():
    def __init__(self, name, balance, hand, folded):
        self.name = name
        self.balance = balance
        self.hand = []
        self.folded = folded
    def getBalance(self):
        return self.balance
    def addBalance(self, amount):
        self.balance += amount
    def reduceBalance(self, amount):
        self.balance -= amount
    
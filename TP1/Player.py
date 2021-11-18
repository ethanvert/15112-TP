from Deck import *
import random, time

class Player:
    def __init__(self, hand, position, name):
        self.hand = hand
        self.position = position
        self.name = name
        self.playing = True
        self.balance = 2000
        self.handScore = 0

    def __repr__(self):
        return (f"I am {self.name} sitting at {self.position}, with hand" + 
                f"{str(self.hand)} and {self.balance} chips")

    # calling a bet
    def call(self, bet):
        print(f"{self.name} called")
        # checks to see if player has enough to call
        if (self.balance - bet) >= 0:
            self.balance -= bet # decreases balance by bet
            return bet # returns value of call
        else: # bet is too big
            ret = self.balance # player goes all in
            self.balance = 0 
            return ret

    def bet(self, bet):
        if bet <= self.balance:
            self.balance -= bet
        else:
            return self.balance
        return bet

    def fold(self):
        print(f"{self.name} folded")
        self.playing = False
        return 0

    def check(self):
        print(f"{self.name} checked")
        return 0

class Bot(Player):
    names = ["Bill", "Nancy", "John", "Steven", "Chris", "Jane", "Alex"]
    def __init__(self, hand, position, name):
        super().__init__(hand, position, name)
        self.difficulty = random.randint(0,1)
        self.minimumPlayable = 2
        self.name = name

    def __repr__(self):
        return (f"I am level {self.difficulty}, sitting at {self.position}" + 
                f" and my hand is {str(self.hand)} with {self.balance} chips")
    
    # next 2 methods for tp2

    # def __Rank(self, board):
    #     pass

    # def calculateHandStrength(self, board):
    #     if board == None:
    #         if self.__Rank()>10:
    #             pass

    def bet(self):
        print(f"{self.name} betted")
        return random.randint(10,50)

    def playHand(self, board, bet=0):
        time.sleep(1)
        move = random.randint(1,4)
        if move == 1:
            return self.call(bet)
        elif move == 2:
            return self.check()
        elif move == 3:
            return self.fold()
        else:
            return self.check()
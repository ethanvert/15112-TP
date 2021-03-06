from Deck import *
import random, time

class Player:
    def __init__(self, hand, position, name):
        self.hand = hand
        self.position = position
        self.name = name
        self.playing = True
        self.played = False
        self.balance = 2000
        self.handScore = 0

    def __repr__(self):
        return (f"I am {self.name} sitting at {self.position}, with hand" + 
                f"{str(self.hand)} and {self.balance} chips")

    # calling a bet
    def call(self, bet):
        # checks to see if player has enough to call
        if (self.balance - bet) >= 0:
            self.balance -= bet # decreases balance by bet
            print(f"here with a balance of {self.balance}")
            return bet, f"{self.name} called" # returns value of call
        else: # bet is too big
            ret = self.balance # player goes all in
            self.balance = 0 
            return ret, f"{self.name} called"

    def bet(self, bet):
        if bet <= self.balance:
            self.balance -= bet
        else:
            return self.balance
        return bet, f"{self.name} bets {bet} chips"

    def fold(self):
        self.playing = False
        return 0, f"{self.name} folded"

    def check(self):
        return 0, f"{self.name} checked"

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

    def playHand(self, board, bet = 0):
        time.sleep(1)
        move = random.randint(1,4)
        if move == 1:
            return self.fold()
        elif move == 2:
            return self.fold()
        elif move == 3:
            return self.fold()
        else:
            return self.fold()
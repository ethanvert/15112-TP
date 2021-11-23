from Deck import *
import random, time, copy

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
    
    #next 2 methods for tp2

    def preFlopRank(self):
        rank = 0
        if self.hand[0].suit == self.hand[1].suit:
            rank += 10

        if self.hand[0].number == self.hand[1].number:
            rank += self.hand[0].number 

        if (Deck.numberScoreMap[self.hand[0].number] > 10 and 
            Deck.numberScoreMap[self.hand[0].number] > 10):
            rank += 
        return rank

    def calculateOuts(self, board):
        tempBoard = copy.deepCopy(board)
        tempBoard.append(self.hand[0])
        tempBoard.append(self.hand[1])
        numOuts = 0

        scoreDict = dict()

        for number in PlayingCard.numberNames:
            for suit in PlayingCard.numberNames:
                currentCard = PlayingCard(number, suit)
                if currentCard in tempBoard:
                    continue
                else:
                    tempBoard.append(currentCard)
                    if len(board) == 4:
                        score = Deck.calculateHandScore(self.hand, tempBoard)
                        scoreDict[currentCard] = scoreDict.get(currentCard, 
                                                                score)
                    else:
                        pass
                    tempBoard.pop()
                        
        for card in scoreDict:
            

                
                
                

                    

    def calculateHandStrength(self, board):
        if board == None:
            if self.preFlopRank()> 10:
                self.bet(30)
            elif self.preFlopRank() > 
    
    def calculateOddsToWin(self, board):
        numOfOuts = self.calculateOuts(board)
        




    def calculatePotOdds(self, bet, pot):
        return pot/bet

    def playHand(self, board, pot, bet = 0):
        time.sleep(1)
        potOdds = self.calculatePotOdds(bet, pot)
        
        if board == [ ]:
            calculateHandStrength(board)
        else:
            odds = self.calculateOddsToWin(board)
            if odds > potOdds:
                self.call(bet)
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
        self.tightness = random.randint(1,3)
        self.minimumPlayable = 2
        self.name = name

    def __repr__(self):
        return (f"I am level {self.difficulty}, sitting at {self.position}" + 
                f" and my hand is {str(self.hand)} with {self.balance} chips")
    
    #next 2 methods for tp2

    def preFlopRank(self):
        rank = 0
        card1Number = Deck.numberScoreMap[self.hand[0].number]
        card2Number = Deck.numberScoreMap[self.hand[1].number]
        card1Suit = self.hand[0].suit
        card2Suit = self.hand[1].suit

        if card1Suit == card2Suit: # suited cards
            rank += 4
        if self.hand[0].number == self.hand[1].number: # pocket pair
            rank += 14 + card1Number * 2
        else: # anything else
            rank += (card1Number + card2Number)/1.5
        
        return rank

    def calculateOuts(self, board):
        tempBoard = copy.deepcopy(board)
        tempBoard.append(self.hand[0])
        tempBoard.append(self.hand[1])
        numOuts = 0
        maxScore = 0

        scoreDict = dict()

        for number in PlayingCard.numberNames:
            for suit in PlayingCard.numberNames:
                currentCard = PlayingCard(number, suit)
                if currentCard in tempBoard:
                    continue
                else:
                    tempBoard.append(currentCard)
                    score = Deck.calculateHandScore(self.hand, tempBoard)
                    scoreDict[currentCard] = scoreDict.get(currentCard, 
                                                                score)
                    if score > maxScore:
                        maxScore = score
                    tempBoard.pop()
                        
        for card in scoreDict:
            if (maxScore[0] - scoreDict[card][0] <= 14 and 
                maxScore[1] == scoreDict[card][1]):
                numOuts += 1
        return numOuts     

    def calculateHandStrength(self, board):
        if board == None:
            if self.preFlopRank() > 10:
                self.bet(30)
            elif self.preFlopRank() > 10:
                pass
        return 15

    def calculateOddsToWin(self, board):
        numOfOuts = self.calculateOuts(board)
        if len(board) == 3:
            return numOfOuts/100 * 2
        elif len(board) == 4:
            return numOfOuts/100

    def calculatePotOdds(self, bet, pot):
        return bet/pot

    # finds hands to beat the bot's
    def calculateBeats(self, board):
        beats = [ ]
        hand = [ ]
        handScore = Deck.calculateHandScore(self.hand, board)

        # loops through every combination of two cards that beat the bot's hand
        for number in PlayingCard.numberNames:
            for suit in PlayingCard.suitNames:
                if PlayingCard(number, suit) in board:
                    continue
                else:
                    hand.append(PlayingCard(number, suit))

                    for number2 in PlayingCard.numberNames:
                        for suit2 in PlayingCard.suitNames:
                            if PlayingCard(number, suit) in board:
                                continue
                            else:
                                hand.append(PlayingCard(number, suit))

                                if (Deck.calculateHandScore(hand, board) > 
                                    handScore):
                                    beats.append(copy.deepcopy(board) + hand)
                                hand.pop()
                    hand.pop()

        return beats

    def playHand(self, board, pot, bet = 0):
        time.sleep(1)
        move = random.randint(1,4)
        if move == 1:
            return self.check()
        elif move == 2:
            return self.call(bet)
        elif move == 3:
            return self.bet(10)
        else:
            return self.fold()

    # WIP
    # def playHand(self, board, pot, bet = 0):
    #     time.sleep(1)
    #     potOdds = self.calculatePotOdds(bet, pot)
        
    #     if board == [ ]:
    #         preFlopStrength = self.preFlopRank()
    #         if bet > 0:
    #             if preFlopStrength > 24:
    #                 return self.bet(bet * 3)
    #             elif preFlopStrength > 20:
    #                 return self.bet(bet * 2)
    #             elif preFlopStrength > 16:
    #                 return self.call(bet)
    #             else:
    #                 return self.fold()
    #     else:
    #         if self.calculateHandStrength(board) > 14:
    #             beats = self.calculateBeats(board)

    #             if len(beats) <= 10 / self.tightness:
    #                 if bet > 0:
    #                     return self.call(bet)
    #                 else:
    #                     if len(beats) <= 10 / self.tightness * 1:
    #                         return self.bet(10)
    #                     elif len(beats) <= 10 / self.tightness * 2:
    #                         return self.bet(pot//2)
    #                     elif len(beats) <= 10 / self.tightness * 3:
    #                         return self.bet(pot)
    #             else:
    #                 if bet > 0:
    #                     return self.fold()
    #                 else:
    #                     return self.check()
    #         else:
    #             odds = self.calculateOddsToWin(board)
    #             if bet > 0:
    #                 if odds > potOdds:
    #                     return self.call(bet)
    #                 else:
    #                     return self.fold()
    #             else:
    #                 if odds > self.tightness * .25:
    #                     return self.bet(pot)
    #                 elif odds > self.tightness * .20:
    #                     return self.bet(pot//2)
    #                 elif odds > self.tightness * .15:
    #                     return self.bet(10)
    #                 else:
    #                     return self.check()
                
###########################
# Contains Player class and Bot subclass. Player class contains all information about
# a certain user, and the Bot subclass adds on the necessary attributes and methods
# for any bot to play any hand.
###########################

from Deck import *
import random, time, copy

class Player:
    def __init__(self, hand, position, name):
        self.hand = hand
        self.position = position
        self.name = name
        self.playing = True
        self.played = False
        self.currentBet = 0
        self.balance = 2000
        self.handScore = 0
        self.deck = Deck()

    def __repr__(self):
        return (f"I am {self.name} sitting at {self.position}, with hand" + 
                f"{str(self.hand)} and {self.balance} chips")

    # calling a bet
    def call(self, bet):
        # checks to see if player has enough to call
        if (self.balance - bet) >= 0:
            self.balance -= bet - self.currentBet # decreases balance by bet
            self.currentBet += bet - self.currentBet
            return (bet - self.currentBet), f"{self.name} called" # returns value of call
        else: # bet is too big
            ret = self.balance # player goes all in
            self.balance = 0 
            return ret, f"{self.name} called"

    def bet(self, amount, currentBet=0):
        if amount <= self.balance:
            self.balance -= amount + currentBet
            self.currentBet += amount + currentBet
        else:
            self.currentBet += self.balance
            return self.balance, f"{self.name} goes all in"
        return amount, f"{self.name} raises ${amount}."

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
        return (f"I am {self.name}, level {self.tightness}, sitting at {self.position}" + 
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
            rank += 7 + card1Number * 2
        else: # anything else
            rank += (card1Number + card2Number)/1.5
        
        return rank

    def calculateOuts(self, board):
        tempBoard = copy.deepcopy(board)
        tempBoard.append(self.hand[0])
        tempBoard.append(self.hand[1])
        numOuts = 0
        maxScore = (0,"")

        scoreDict = dict()

        for number in PlayingCard.numberNames:
            for suit in PlayingCard.suitNames:
                currentCard = PlayingCard(number, suit)
                if currentCard in tempBoard:
                    continue
                else:
                    tempBoard.append(currentCard)
                    score = self.deck.calculateHandScore(self.hand, tempBoard)
                    scoreDict[currentCard] = scoreDict.get(currentCard, score)
                    if score[0] > maxScore[0]:
                        maxScore = score
                    tempBoard.pop()
                        
        for card in scoreDict:
            if (maxScore[0] - scoreDict[card][0] <= 14 and 
                maxScore[1] == scoreDict[card][1]):
                numOuts += 1
        return numOuts     

    def calculateHandStrength(self, board):
        handScore = self.deck.calculateHandScore(self.hand, board)
        return handScore[0]

    def calculateOddsToWin(self, board):
        numOfOuts = self.calculateOuts(board)

        if len(board) == 3:
            return numOfOuts/100 * 2
        elif len(board) == 4:
            return numOfOuts/100 
        else:
            return numOfOuts/100

    def calculatePotOdds(self, bet, pot):
        return bet/pot

    # finds hands to beat the bot's
    def calculateBeats(self, board):
        beats = [ ]
        hand = [ ]
        handScore = self.deck.calculateHandScore(self.hand, board)

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
                                hand.append(PlayingCard(number2, suit2))

                                if (self.deck.calculateHandScore(hand, board) > 
                                    handScore):
                                    beats.append(copy.deepcopy(board) + hand)
                                hand.pop()
                    hand.pop()

        return beats

    def playHand(self, board, pot, numPlayers, bet=0):
        time.sleep(1)
        potOdds = self.calculatePotOdds(bet, pot)
        
        if board == [ ]:
            preFlopStrength = self.preFlopRank()

            if bet > 0 and self.position <= numPlayers // 3:
                if preFlopStrength > 24:
                    return self.bet(bet * 3, bet)
                elif preFlopStrength > 20:
                    return self.bet(bet * 2, bet)
                elif preFlopStrength > 16:
                    return self.call(bet)
                else:
                    return self.fold()
            elif (self.position <= numPlayers-1 and 
                  self.position >= numPlayers - numPlayers // 3):
                if bet == 10:
                    return self.call(bet)
                elif bet > 10:
                    if preFlopStrength > 22:
                        return self.bet(bet * 3, bet)
                    elif preFlopStrength > 18:
                        return self.bet(bet * 2, bet)
                    elif preFlopStrength > 14:
                        return self.call(bet)
                    else:
                        return self.fold()
            else:
                if preFlopStrength > 20:
                    return self.bet(bet * 3, bet)
                elif preFlopStrength > 16:
                    return self.bet(bet * 2, bet)
                elif preFlopStrength > 12:
                    return self.call(bet)
                else:
                    return self.fold()
        else:
            if self.calculateHandStrength(board) > 14:
                beats = self.calculateBeats(board)

                if len(beats) <= 10 / self.tightness:
                    if bet > 0:
                        return self.call(bet)
                    else:
                        if len(beats) <= 10 / self.tightness * 1:
                            return self.bet(10, bet)
                        elif len(beats) <= 10 / self.tightness * 2:
                            return self.bet(pot//2, bet)
                        elif len(beats) <= 10 / self.tightness * 3:
                            return self.bet(pot, bet)
                else:
                    if bet > 0:
                        return self.fold()
                    else:
                        return self.check()
            else:
                if len(board) < 5:
                    if (self.calculateHandStrength(board) > 
                                                   30 + (self.tightness * 4.6)):
                        if bet > 0:
                            if (self.calculatePotOdds(bet, pot) > 
                            1/(4 + self.tightness)):
                                return self.bet(bet * 3, bet)
                            elif (self.calculatePotOdds(bet, pot) > 
                                                        1/(3 + self.tightness)):
                                return self.bet(bet * 2, bet)
                            elif (self.calculatePotOdds(bet, pot) > 
                                                            1/(self.tightness)):
                                decision = random.randint(0,1)
                                if decision:
                                    return self.call(bet)
                                else:
                                    return self.fold()
                        else:
                            if self.tightness == 3:
                                if (self.calculateHandStrength(board) > 
                                                 55.4 + (self.tightness * 4.6)):
                                    return self.bet(pot//3, bet)
                                elif (self.calculateHandStrength(board) > 
                                                 70.4 + (self.tightness * 4.6)):
                                    return self.bet(pot//2, bet)
                                elif (self.calculateHandStrength(board) > 
                                                 85.4 + (self.tightness * 4.6)):
                                    return self.bet(pot, bet)
                                elif (self.calculateHandStrength(board) > 
                                                100.4 + (self.tightness * 4.6)):
                                    return self.bet(self.balance, bet)
                                else:
                                    return self.check()
                            elif self.tightness == 2:
                                if (self.calculateHandStrength(board) > 
                                                 40.4 + (self.tightness * 4.6)):
                                    return self.bet(pot//3, bet)
                                elif (self.calculateHandStrength(board) > 
                                                 55.4 + (self.tightness * 4.6)):
                                    return self.bet(pot//2, bet)
                                elif (self.calculateHandStrength(board) > 
                                                 70.4 + (self.tightness * 4.6)):
                                    return self.bet(pot, bet)
                                elif (self.calculateHandStrength(board) > 
                                                85.4 + (self.tightness * 4.6)):
                                    return self.bet(self.balance, bet)
                                else:
                                    return self.check()
                            else:
                                if (self.calculateHandStrength(board) > 
                                                 25.4 + (self.tightness * 4.6)):
                                    return self.bet(pot//3, bet)
                                elif (self.calculateHandStrength(board) > 
                                                 40.4 + (self.tightness * 4.6)):
                                    return self.bet(pot//2, bet)
                                elif (self.calculateHandStrength(board) > 
                                                 55.4 + (self.tightness * 4.6)):
                                    return self.bet(pot, bet)
                                elif (self.calculateHandStrength(board) > 
                                                70.4 + (self.tightness * 4.6)):
                                    return self.bet(self.balance, bet)
                                else:
                                    return self.check()
                    else:
                        odds = self.calculateOddsToWin(board)

                        if bet > 0:
                            if odds > potOdds:
                                return self.call(bet)
                            else:
                                return self.fold()
                        else:
                            if odds > self.tightness * .20:
                                return self.bet(pot, bet)
                            elif odds > self.tightness * .15:
                                return self.bet(pot//2, bet)
                            elif odds > self.tightness * .10:
                                return self.bet(10, bet)
                            else:
                                return self.check()
                else:
                    beats = self.calculateBeats(board)

                    if len(beats) <= 10 / self.tightness:
                        if bet > 0:
                            if self.calculatePotOdds(bet, pot) > 1/(4 + self.tightness):
                                return self.bet(bet * 3, bet)
                            elif self.calculatePotOdds(bet, pot) > 1/(3 + self.tightness):
                                return self.bet(bet * 2, bet)
                            else:
                                return self.call(bet)
                        else:
                            if len(beats) <= 10 / self.tightness * 1:
                                return self.bet(10, bet)
                            elif len(beats) <= 10 / self.tightness * 2:
                                return self.bet(pot//2, bet)
                            elif len(beats) <= 10 / self.tightness * 3:
                                return self.bet(pot, bet)
                            else:
                                return self.check()
                    else:
                        if bet > 0:
                            return self.fold()
                        else:
                            return self.check()
#####################
# Contains PokerGame class with all of the attributes and methods pertaining to the
# a specific game being played.
#####################

from Deck import *
from Player import *

class PokerGame:
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers
        self.smallBlind, self.bigBlind = 5, 10
        self.players = { }
        self.names = [ ]
        self.pot = 0
        self.deck = Deck()
        self.gameOver = False
        self.dealt = True
        self.currentBet = 0
        self.numPlaying = 0


    def dealHand(self):
        hand = (self.deck.deck.pop(), self.deck.deck.pop())
        return hand

    def dealFlop(self):
        self.deck.deck.pop()
        return [self.deck.deck.pop(), self.deck.deck.pop(), 
                    self.deck.deck.pop()]

    def dealTurnOrRiver(self):
        self.deck.deck.pop()
        return self.deck.deck.pop()
    
    def removeLosers(self):
        for name in self.names:
            if self.players[name].balance <= 0:
                self.eliminatePlayer(name)
    def eliminatePlayer(self, name):
        del self.players[name]

    def addPlayer(self, player):
        if player.name not in self.players:
            self.players[player.name] = player
            self.names.append(player.name)
        self.numPlayers = len(self.players)

    def collectBlinds(self):
        for player in self.players:
            if self.players[player].position == len(self.players)-2:
                self.players[player].bet(self.smallBlind)
                self.players[player].currentBet = self.smallBlind
                self.pot += self.smallBlind
            elif self.players[player].position == len(self.players)-1:
                self.players[player].bet(self.bigBlind) 
                self.players[player].currentBet = self.bigBlind
                self.pot += self.bigBlind
        self.currentBet = self.bigBlind

    def bet(self, amount):
        if amount < self.bigBlind or amount < 2 * self.currentBet:
            return 1
            
        self.currentBet += amount - self.currentBet
        self.pot += amount

    def call(self, amount):
        self.pot += amount
        #will add logic for sidepot later

    def getWinner(self, board):
        scores = dict()
        highScore = (0,'')
        playing = self.getNumberPlaying()[1]

        for name in playing:
            hand = self.players[name].hand
            score = self.deck.calculateHandScore(hand, board)
            if score[0] > highScore[0]:
                highScore = score
            self.players[name].handScore = score[0]

            if score[0] not in scores:
                scores[score[0]] = [name]
            else:
                scores[score[0]].append(name)

        return scores[highScore[0]], highScore[1]

    # returns the number of players playing during current hand
    def getNumberPlaying(self):
        numPlaying = 0
        players = [ ]
        for player in self.players:
            if self.players[player].playing:
                numPlaying += 1
                players.append(player)
        return numPlaying, players

    # when betting is over, sets current bet to 0
    def nextStage(self):
        self.currentBet = 0
        for player in self.players:
            self.players[player].played = False        

    # when hand is over, resets these variables for next hand
    def newRound(self):
        self.deck = Deck()
        self.numPlayers = len(self.players)
        for player in self.players:
            self.players[player].playing = True
            self.players[player].played = False
            self.players[player].position = ((self.players[player].position - 1)
                                                % len(self.players))
            self.players[player].handScore = 0
            self.players[player].currentBet = 0
        self.gameOver = False
        self.dealt = False
        self.currentBet = 0
        self.pot = 0 
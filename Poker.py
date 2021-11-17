# Note: I got heavy inspiration for the hand scoring algo from https://towardsdatascience.com/poker-with-python-how-to-score-all-hands-in-texas-holdem-6fd750ef73d

from cmu_112_graphics import *
import random
import math
import time 

class PokerGame:
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers
        self.smallBlind, self.bigBlind = 1, 2
        self.players = { }
        self.pot = 0
        self.deck = Deck()
        self.gameOver = False
        self.currentBet = 0

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
    
    def eliminatePlayer(self, name):
        del self.players[name]

    def addPlayer(self, player):
        self.players[player.name] = player

    def bet(self, amount):
        if amount < self.bigBlind or amount < 2 * self.currentBet:
            return 1
        self.currentBet = amount
        self.pot += amount

    def call(self, amount):
        self.pot += amount
        #will add logic for sidepot later

    def getWinner(self, board):
        scores = dict()
        highScore = 0
        for name in self.players:
            score = self.players[name].handScore
            scores[score] = scores.get(score, "") + name
        highScore = max(scores)

        return scores[highScore]

    def nextStage(self):
        self.currentBet = 0

    def newRound(self):
        for player in self.players:
            self.players[player].folded = False
            self.players[player].handScore = 0
        self.deck = Deck()
        self.gameOver = False
        self.currentBet = 0
        self.pot = 0 

# from notes
class PlayingCard:
    numberNames = [None, "Ace", "2", "3", "4", "5", "6", "7",
                   "8", "9", "10", "Jack", "Queen", "King"]
    suitNames = ["Clubs", "Diamonds", "Hearts", "Spades"]
    cardImageMap = {}
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3

    def __init__(self, number, suit):
        # number is 1 for Ace, 2...10,
        #           11 for Jack, 12 for Queen, 13 for King
        # suit is 0 for Clubs, 1 for Diamonds,
        #         2 for Hearts, 3 for Spades
        self.number = number
        self.suit = suit

    def __repr__(self):
        number = PlayingCard.numberNames[self.number]
        suit = PlayingCard.suitNames[self.suit]
        return f'<{number} of {suit}>'


class Deck:
    numberScoreMap = {"2" : 2, "3" : 3, "4" : 4, "5" : 5, "6" : 6, "7" : 7,
                   "8" : 8, "9" : 9, "10" : 10, "Jack" : 11, "Queen" : 12, 
                   "King" : 13, "Ace" : 14}
    suitMap = {"Clubs" : "c", "Diamonds" : "d", "Hearts" : "h", "Spades" : "s"}
    def __init__(self):
        self.deck = self.getDeck()
    
    def __repr__(self):
        return f"Hi This is the deck {self.deck}"
    
    # from notes
    def getDeck(shuffled=True):
        deck = [ ]
        for number in range(1, 14):
            for suit in range(4):
                deck.append(PlayingCard(number, suit))
        if (shuffled):
            random.shuffle(deck)
        return deck

    def getHighCardScore(self, numbers):
        score = (numbers[0] + numbers[1] * .1 + numbers[2] * .01 + 
                 numbers[3] * .001 + numbers[4] * .0001)
        return score

    def getPairScore(self, numbers):
        pair = 0
        score = 15
        exp = 0

        for n in numbers:
            if numbers.count(n) == 2:
                pair = n
            else:
                exp += 1
                score += n / (10**exp)
        return score + pair

    def getTwoPairScore(self, numbers):
        pairs = set()
        score = 30
        exp = 0

        for n in numbers:
            if numbers.count(n) == 2:
                pairs.add(n)
            else:
                exp += 1 
                score += n / (10**exp)
        
        for elem in pairs:
            score += elem
        
        return score
        
    def getThreeOfAKindScore(self, numbers):
        three = 0
        score = 45
        exp = 0

        for n in numbers:
            if numbers.count(n) == 3:
                three = n
            else:
                exp += 1
                score += n / (10**exp)
        return score + three

    def getStraightScore(self, numbers):
        score = 60
        return score + max(numbers)

    def getFlushScore(self, numbers):
        score = 75
        return self.getHighCardScore(self, numbers)

    def getFullHouseScore(self, numbers):
        score = 90
        triple = 0
        pair = 0

        for n in numbers:
            if numbers.count(n) == 3:
                triple = n
            else:
                pair = n

        score += triple + pair / 10

        return score

    def getQuadsScore(self, numbers):
        score = 105
        quad = 0
        
        for n in numbers:
            if numbers.count(n) == 4:
                quad = n
            else:
                score += n / 10
        return score + quad

    def getStraightFlushScore(self, numbers):
        score = 120
        high = max(numbers)

        return score + high   

class Player:
    def __init__(self, hand, position, name):
        self.hand = hand
        self.position = position
        self.name = name
        self.folded = False
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
            return bet # returns value of call
        else: # bet is too big
            ret = self.balance # player goes all in
            self.balance = 0 
            return ret

    def bet(self, bet):
        self.balance -= bet
        return bet

    def fold(self):
        self.folded = True
        return 0

    def check(self):
        return 0

    def getHandNumbers(self, board):
        nums = [ Deck.numberScoreMap[c.number] for c in self.hand ]
        for card in board:
            num = Deck.numberScoreMap[card.number]
            nums.append(num)
        
        return nums

    def getHandSuits(self, board):
        suits = [ Deck.numberScoreMap[c.suit] for c in self.hand ]
        for card in board:
            suit = Deck.numberScoreMap[card.suit]
            suits.append(suit)
        
        return suits

    def getNumCounts(L):
        counts = dict()

        for num in L:
            counts[L.count(num)] = counts.get(L.count(num), set())
            counts[L.count(num)].add(num)

        return counts

    def getSuitCounts(L):
        counts = dict()

        for suit in L:
            counts[L.count(suit)] = counts.get(L.count(suit), set())
            counts[L.count(suit)].add(suit)     

        return counts      

    def calculateHandScore(self, board):
        numbers = self.getHandNumbers(self.hand, board)
        suits = self.getHandSuits(self.hand, board)
        numCounts = self.getNumCounts(numbers)
        suitCounts = self.getSuitCounts(suits)
        hand = ""

        if 5 in suitCounts:
            if len(numCounts) == 1 and max(numbers) - min(numbers) == 4:
                hand = "Straight Flush"
                score = Deck.getStraightFlushScore(numbers)
            else:
                hand = "Flush"
                score = Deck.getFlushScore(numbers)
        else:
            if 4 in numCounts:
                hand = "Four of a Kind"
                score = Deck.getQuadsScore(numbers)
            elif 3 in numCounts and 2 in numCounts:
                hand = "Full House"
                score = Deck.getFullHouseScore(numbers)
            elif len(numCounts) == 1 and max(numbers) - min(numbers) == 4:
                hand = "Straight"
                score = Deck.getStraightScore(numbers)
            elif 3 in numCounts:
                hand = "Three of a Kind"
                score = Deck.getThreeOfAKindScore(numbers)
            elif 2 in numCounts and len(numCounts[2]) > 1:
                hand = "Two Pair"
                score = Deck.getTwoPairScore(numbers)
            elif 2 in numCounts:
                hand = "Pair"
                score = Deck.getPairScore(numbers)
            else:
                hand = "High Card"
                score = Deck.getHighCardScore(numbers)

        self.handScore = score
        return (score, hand)

class Bot(Player):
    names = ["Bill", "Nancy", "John", "Steven"]
    def __init__(self, hand, position, name):
        super().__init__(hand, position, name)
        self.difficulty = random.randint(0,1)
        self.minimumPlayable = 2
        self.name = name

    def __repr__(self):
        return (f"I am level {self.difficulty}, sitting at {self.position}" + 
                f" and my hand is {str(self.hand)} with {self.balance} chips")
   
    def __Rank(self, board):
        pass

    def calculateHandStrength(self, board):
        if board == None:
            if self.__Rank()>10:
                pass

    def bet(self):
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
            return self.bet()

###########
# Start Screen
###########
def splash_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = "dark green")
    canvas.create_text(app.width/2, app.height/2, font = "Arial 26",
                        text = "Press any key to play!")

def splash_keyPressed(app, event):
    app.mode = "game"

##########
# Game
#########
def game_newPlayer(app):
    hand = app.game.dealHand()
    if len(app.game.players) == 0:
        name = "Ethan"
        print(name)
        app.game.addPlayer(Player(hand, len(app.game.players), name))
    else:
        name = Bot.names[random.randint(0,3)]
        print(name)
        app.game.addPlayer(Bot(hand, len(app.game.players), name))
    
def game_keyPressed(app, event):
    if event.key == "Enter":
        app.play = True
    if event.key == "Escape":
        app.mode = "pause"
    if event.key == "Up":
        game_newPlayer(app)

def game_playerMove(app, name):
    if app.game.currentBet > 0:
        move = app.getUserInput("Call, bet, or fold?")
        if move == "Call" or "call":
            app.game.players[name].call(app.game.currentBet)
        elif move == "Bet" or move == "bet":
            bet = int(app.getUserInput("How much would you like to bet?"))
            app.game.bet(bet)
            app.game.players[name].bet(bet)
        elif move == "Fold" or move == "fold":
            app.game.players[name].fold()
    else:
        move = app.getUserInput("Check, bet, or fold?")
        print(move)
        if move == "Check" or move == "check":
            app.game.players[name].check()
        elif move == "Bet" or move == "bet":
            bet = int(app.getUserInput("How much would you like to bet?"))
            app.game.bet(bet)
            app.game.players[name].bet(bet)
        elif move == "Fold" or move == "fold":
            app.game.players[name].fold()

def game_botMove(app, name):
    if app.game.currentBet> 0:
        app.game.players[name].call(app.game.currentBet)
    move = app.game.players[name].playHand(app.board)
    if move > 0:
        if app.game.bet(move) != None:
            game_botMove(app, name)
        else:
            app.game.bet(move)

def game_playRound(app):
    for name in app.game.players:
        print(name +" is a " + str(type(app.game.players[name])))
        if (type(app.game.players[name]) == Player and 
            not app.game.players[name].folded):
            print("hand: ", app.game.players[name].hand)
            game_playerMove(app, name)
        elif (type(app.game.players[name]) == Bot and 
            not app.game.players[name].folded):
            game_botMove(app, name)

def game_playPreFlop(app):
    app.game.nextStage()
    game_playRound(app)
    print(f"The pot has {app.game.pot} chips")
    app.turn += 1
    app.stage = app.turn % 4

def game_playFlop(app):
    app.game.nextStage()
    app.board += app.game.dealFlop()
    print("--------------------")
    print(app.board)
    print(f"The pot has {app.game.pot} chips")  
    game_playRound(app)          
    app.turn += 1
    app.stage = app.turn % 4

def game_playTurn(app):
    app.game.nextStage()
    app.board.append(app.game.dealTurnOrRiver())
    print("--------------------")
    print(app.board)
    print(f"The pot has {app.game.pot} chips")
    game_playRound(app)
    app.turn += 1
    app.stage = app.turn % 4

def game_playRiver(app):
    app.game.nextStage()
    app.board.append(app.game.dealTurnOrRiver())
    print("--------------------")
    print(app.board)
    print(f"The pot has {app.game.pot} chips")
    game_playRound(app)
    app.game.getWinner(app.board)
    app.turn += 1
    app.stage = app.turn % 4

def game_timerFired(app):
    if app.game.gameOver: app.stage = "gameOver"

    if app.turn > 0 and app.stage == 0:
        app.game.newRound()
        app.board = [ ]
    
    for player in app.game.players:
        if app.game.players[player].balance == 0:
            app.game.eliminatePlayer(player)

    if len(app.game.players) > 1:    
        if app.stage == 0:
            game_playPreFlop(app)
        elif app.stage == 1:
            game_playFlop(app)
        elif app.stage == 2:
            game_playTurn(app)
        elif app.stage == 3:
            game_playRiver(app)
        
def game_drawFelt(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = "dark green")

def game_drawCard(app, canvas, x, y):
    canvas.create_image(x, y, 
    image= ImageTk.PhotoImage(app.scaleImage(app.cardImage, 1/10)))

def game_drawNames(app, canvas):
    index = 0
    for name in app.game.players:
        canvas.create_text(app.width/2, app.height/2+100*index, 
                            font = "arial 26",
                            text = str(app.game.players[name]))
        index += 1

def game_redrawAll(app, canvas):
    game_drawFelt(app, canvas)
    game_drawCard(app, canvas, app.width/10, app.height/2)
    game_drawNames(app, canvas)

    for i in range(len(app.game.players)):
        game_drawCard(app, canvas, app.width/2, 0+i*app.height)

###########
# pause
###########

def pause_redrawAll(app, canvas):
    canvas.create_text(app.width/2, app.height/2, font = "Arial 26", 
                        text= "Paused, press enter or esc to resume")

def pause_keyPressed(app, event):
    if event.key == "Enter" or event.key == "Escape":
        app.mode = "game"
    if event.key == "h":
        app.mode = "help"

###############
# help
##############
def help_redrawAll(app, canvas):
    canvas.create_text(app.width/2, app.height/2, font = "Arial 26", 
                        text= "What do you need help with?")
##############
# Main Stuff
##############
def appStarted(app):
    url = ("https://s3.amazonaws.com/images.penguinmagic.com/"
            +"images/products/original/8006b.jpg")
    app.cardImage = app.loadImage(url)
    app.mode = "splash"
    app.numPlayers = 2
    app.board = [ ]
    app.proceed = False
    app.play = False
    app.turn = 0
    app.stage = app.turn % 3
    app.game = PokerGame(app.numPlayers)

def playPoker():
    runApp(width=512, height=512)

def main():
    playPoker()

if __name__ == '__main__':
    main()

from cmu_112_graphics import *
import random
import math

class PokerGame:
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers
        self.smallBlind, self.bigBlind = 1, 2
        self.players = { }
        self.pot = 0
        self.deck = Deck()
        self.gameOver = False
        self.hasBet = False
        self.currentBet = 0

    def dealHand(self):
        hand = (self.deck.deck.pop(), self.deck.deck.pop())
        return hand

    def dealFlop(self):
        self.deck.deck.pop()
        return [self.deck.deck.pop(), self.deck.deck.pop(), self.deck.deck.pop()]

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
        self.hasBet = True
        self.currentBet = amount
        self.pot += amount

    def nextStage(self):
        self.currentBet = 0
        self.hasBet = False

    def newRound(self):
        self.deck = Deck()
        self.gameOver = False
        self.currentBet = 0
        self.pot = 0
                

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
    def __init__(self):
        self.deck = self.getDeck()
    
    def __repr__(self):
        return f"Hi This is the deck {self.deck}"
    
    def getDeck(shuffled=True):
        deck = [ ]
        for number in range(1, 14):
            for suit in range(4):
                deck.append(PlayingCard(number, suit))
        if (shuffled):
            random.shuffle(deck)
        return deck

class Player:
    def __init__(self, hand, position, name):
        self.hand = hand
        self.position = position
        self.name = name
        self.folded = False
        self.balance = 2000

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

    def fold(self):
        self.folded = True
    
    def check(self):
        pass

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
        return random.randint(1,5)

    def playHand(self, board):
        move = random.randint(1,4)
        if move == 1:
            return self.call()
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
    if app.game.bet:
        move = app.getUserInput("Call, bet, or fold?")
    else:
        move = app.getUserInput("Check, bet, or fold?")
        if move == "Check" or "check":
            app.game.players[name].check()
        elif move == "Bet" or "bet":
            bet = app.getUserInput("How much would you like to bet?")
            app.game.players[name].bet(bet)
        elif move == "Fold" or "fold":
            app.game.players[name].fold()

def game_botMove(app, name):
    move = app.game.players[name].playHand(app.board)
    if move > 0:
        if app.game.bet(move) != None:
            game_botMove(app, name)
    

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

def game_timerFired(app):
    if app.game.gameOver: return

    print(app.stage)
    if app.turn > 0 and app.stage == 0:
        app.game.newRound()
        app.board = [ ]
        
    if app.proceed:
        if app.stage == 0:
            if app.play:
                game_playRound(app)
                app.proceed = False
        elif app.stage == 1:
            app.board += app.game.dealFlop()
        elif app.stage == 2 or 3:
            app.board.append(app.game.dealTurnOrRiver())
            print("--------------------")
            print(app.board)
            app.turn += 1
            app.proceed = False
            app.play = True
            app.stage = app.turn % 3
        
def game_drawFelt(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = "dark green")

def game_drawCard(app, canvas, x, y):
    canvas.create_image(x, y, 
    image= ImageTk.PhotoImage(app.scaleImage(app.cardImage, 1/10)))

def game_drawNames(app, canvas):
    for name in app.game.players:
        index = 0
        canvas.create_text(app.width/2, app.height/2+100*index, font = "arial 26",
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
    canvas.create_text(app.width/2, app.height/2, font = "Arial 26", text= "Paused, press enter or esc to resume")

def pause_keyPressed(app, event):
    if event.key == "Enter" or event.key == "Escape":
        app.mode = "game"

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

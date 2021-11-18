# Note: I got heavy inspiration for the hand scoring algo from https://towardsdatascience.com/poker-with-python-how-to-score-all-hands-in-texas-holdem-6fd750ef73d

from cmu_112_graphics import *
from Deck import *
import random
import time 

class PokerGame:
    def __init__(self):
        self.numPlayers = 0
        self.smallBlind, self.bigBlind = 1, 2
        self.players = { }
        self.pot = 0
        self.deck = Deck()
        self.gameOver = False
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
        highScore = (0,'')
        playing = self.getNumberPlaying()[1]

        for name in playing:
            hand = self.players[name].hand
            score = self.deck.calculateHandScore(hand, board)
            if score[0] > highScore[0]:
                highScore = score
            self.players[name].handScore = score[0]
            scores[score[0]] = scores.get(score[0], "") + name

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

    # when hand is over, resets these variables for next hand
    def newRound(self):
        self.deck = Deck()
        for player in self.players:
            self.players[player].playing = True
            self.players[player].handScore = 0
            self.players[player].hand = (self.deck.deck.pop(), 
                                         self.deck.deck.pop())
        self.gameOver = False
        self.currentBet = 0
        self.pot = 0 

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
        app.game.numPlayers += 1
        game_newPlayer(app)

def game_playerMove(app, name):
    if app.game.currentBet > 0:
        move = app.getUserInput("Call, bet, or fold?")
        if move == "Call" or "call":
            app.game.players[name].call(app.game.currentBet)
            app.game.call(app.game.currentBet)
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
    print(f"current bet {app.game.currentBet}")
    if app.game.currentBet> 0:
        app.game.pot += app.game.players[name].call(app.game.currentBet)
    else:
        move = app.game.players[name].playHand(app.board)
        if move > 0:
            if app.game.bet(move) != None:
                game_botMove(app, name)
            else:
                app.game.bet(move)

def game_playStage(app):
    for name in app.game.players:
        print(f"num playing {app.game.getNumberPlaying()[0]}")
        if app.game.getNumberPlaying()[0] == 1:
            break
        if (type(app.game.players[name]) == Player and 
            app.game.players[name].playing):
            game_playerMove(app, name)
        elif (type(app.game.players[name]) == Bot and 
            app.game.players[name].playing):
            game_botMove(app, name)

def game_playPreFlop(app):
    print("--------------------")
    print("playing preflop")
    app.game.nextStage()
    game_playStage(app)
    print(f"The pot has {app.game.pot} chips")
    app.turn += 1
    app.stage = app.turn % 4

def game_playFlop(app):
    print("--------------------")    
    print("playing flop")
    app.game.nextStage()
    app.board += app.game.dealFlop()
    # game_drawBoard(app)
    print(app.board) 
    game_playStage(app)
    print(f"The pot has {app.game.pot} chips")          
    app.turn += 1
    app.stage = app.turn % 4

def game_playTurn(app):
    print("--------------------")
    app.game.nextStage()
    app.board.append(app.game.dealTurnOrRiver())
    # game_drawBoard(app)
    print(app.board)
    game_playStage(app)
    app.turn += 1
    app.stage = app.turn % 4

def game_playRiver(app):
    print("--------------------")
    app.game.nextStage()
    app.board.append(app.game.dealTurnOrRiver())
    #app_drawBoard
    print(app.board)
    game_playStage(app)
    print(f"The pot has {app.game.pot} chips")
    winner = app.game.getWinner(app.board)
    print(f"{winner[0]} wins this hand! with {winner[1]}")
    app.game.players[winner[0]].balance += app.game.pot
    app.turn += 1
    app.stage = app.turn % 4

def game_timerFired(app):
    print(f"turn: {app.turn}")
    print(f"stage: {app.stage}")
    print(f"numPlaying: {app.game.getNumberPlaying()[0]}")
    if app.game.gameOver: app.stage = "gameOver"

    if app.game.numPlayers > 1 and app.game.getNumberPlaying()[0] == 1:
        print(f"players: {app.game.getNumberPlaying()[1]}")
        player = app.game.getNumberPlaying()[1][0]
        app.game.players[player].balance += app.game.pot
        app.turn += (4-app.stage)
        app.stage = 0
        print(f"turn after fold: {app.turn}")

    if app.turn > 0 and app.stage == 0:
        app.game.newRound()
        app.board = [ ]

    # if len(app.game.players) > 1:    
    if app.play:
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

def game_drawBoard(app, canvas):
    if app.board == [ ]:
        pass
    else:
        pass

def game_drawPlayer(app, canvas):
    cardAngle = 90
    cardX = app.width/2
    cardY = app.height
    for name in app.game.players:

        if type(app.game.players[name]) == Player:
            canvas.create_text(app.width/2, app.height-100, 
                                font = "arial 12",
                                text = str(app.game.players[name]))

def game_drawBots(app, canvas):
    for name in app.game.players:
        if type(app.game.players[name]) == Bot:
            canvas.create_text(app)

def game_redrawAll(app, canvas):
    game_drawFelt(app, canvas)
    game_drawCard(app, canvas, app.width/10, app.height/2)
    game_drawBots(app, canvas)
    game_drawBoard(app, canvas)

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
    app.board = [ ]
    app.proceed = False
    app.play = False
    app.turn = 0
    app.stage = app.turn % 3
    app.game = PokerGame()

def playPoker():
    runApp(width=512, height=512)

def main():
    playPoker()

if __name__ == '__main__':
    main()

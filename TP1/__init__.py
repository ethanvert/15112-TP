from cmu_112_graphics import *
from Deck import *
from Player import *
import random
import math

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
        if player.name not in self.players:
            self.players[player.name] = player
        self.numPlayers = len(self.players)

    def bet(self, amount):
        if amount < self.bigBlind or amount < 2 * self.currentBet:
            return 1
        self.currentBet += amount
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
        self.numPlayers = len(self.players)
        for player in self.players:
            self.players[player].playing = True
            self.players[player].handScore = 0
            self.players[player].hand = (self.deck.deck.pop(), 
                                         self.deck.deck.pop())
        self.gameOver = False
        self.currentBet = 0
        self.pot = 0 

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
        name = "Player 1"
        print(name)
        app.game.addPlayer(Player(hand, len(app.game.players), name))
    else:
        name = Bot.names[random.randint(0,6)]
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
            app.game.call(app.game.currentBet)
            app.currentMove = f"{name} calls the bet of {app.game.currentBet}"
        elif move == "Bet" or move == "bet":
            bet = int(app.getUserInput("How much would you like to bet?"))
            app.game.bet(bet)
            app.game.players[name].bet(bet)
            app.currentMove = (f"{name} reraises. " +
                                f"Call {app.game.currentBet} chips to play.")
        elif move == "Fold" or move == "fold":
            app.game.players[name].fold()
            app.currentMove = f"{name} folds."
    else:
        move = app.getUserInput("Check, bet, or fold?")
        print(move)
        if move == "Check" or move == "check":
            app.game.players[name].check()
            app.currentMove = f"{name} checks"
        elif move == "Bet" or move == "bet":
            bet = int(app.getUserInput("How much would you like to bet?"))
            app.game.bet(bet)
            app.game.players[name].bet(bet)
            app.currentMove = (f"{name} bets {app.game.currentBet} chips. " +
                                "Call or Fold?")
        elif move == "Fold" or move == "fold":
            app.game.players[name].fold()
            app.currentMove = f"{name} folds."

def game_botMove(app, name):
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
        if app.game.getNumberPlaying()[0] == 1:
            break
        if (type(app.game.players[name]) == Player and 
            app.game.players[name].playing):
            game_playerMove(app, name)
        elif (type(app.game.players[name]) == Bot and 
            app.game.players[name].playing):
            game_botMove(app, name)

def game_playPreFlop(app):
    app.game.nextStage()
    game_playStage(app)
    app.turn += 1
    app.stage = app.turn % 4
    app.game.nextStage()
    app.board += app.game.dealFlop()

def game_playFlop(app):
    game_playStage(app)    
    app.turn += 1
    app.stage = app.turn % 4
    app.game.nextStage()
    app.board.append(app.game.dealTurnOrRiver())

def game_playTurn(app):
    game_playStage(app)
    app.turn += 1
    app.stage = app.turn % 4
    app.game.nextStage()
    app.board.append(app.game.dealTurnOrRiver())

def game_playRiver(app):
    game_playStage(app)
    winner = app.game.getWinner(app.board)
    app.curentMove = f"{winner[0]} wins this hand! with {winner[1]}"
    app.game.players[winner[0]].balance += app.game.pot
    app.turn += 1
    app.stage = app.turn % 4
    app.play = False

def game_timerFired(app):
    if app.game.gameOver: 
        app.stage = "gameOver"
        return
    # if len(app.game.players) > 1:    
    if app.play:
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
    image= app.scaleImage(app.cardImage1, 1/20)
    photoImage = getCachedPhotoImage(app, image)
    canvas.create_image(x, y, image=photoImage)

def game_drawBoard(app, canvas):
    if app.board == [ ]:
        pass
    else:
        for i in range(len(app.board)):
            num = app.numberMap[app.board[i].number]
            suit = app.suitMap[app.board[i].suit]
            cardWidth = 73
            cardHeight = 98
            cX = cardWidth * num
            cY = cardHeight * suit
            cardSpace = 2
            cardX = app.width/2 - (2 - i) * (cardWidth + cardSpace)
            image = app.cardImage2.crop((cX, cY, 
                                        cX + cardWidth, cY + cardHeight))
            photoImage = getCachedPhotoImage(app, image)
            canvas.create_image(cardX, app.height/2, image = photoImage)

def game_drawPlayers(app, canvas):
    cardAngle = math.pi/2
    centerX = app.width/2
    centerY = app.height/2
    index = 0

    for name in app.game.players:
        if type(app.game.players[name]) == Bot:
            cardAngle += math.pi/4 * index
            numerator = app.width/4 * app.height/4
            denominator = math.sqrt((app.width/4)**2 * math.sin(cardAngle)**2 + 
                                     (app.height/4)**2 * math.cos(cardAngle)**2)
            r = numerator/denominator
            cardX = centerX + r * math.cos(cardAngle)
            cardY = centerY + r * math.sin(cardAngle)
            game_drawCard(app, canvas, cardX, cardY)
        else:
            game_drawPlayerHand(app, canvas, name)
        index += 1

def game_drawPlayerHand(app, canvas, name):
    index = 0
    for card in app.game.players[name].hand:
        num = app.numberMap[card.number]
        suit = app.suitMap[card.suit]
        cardWidth = 73
        cardHeight = 98
        cX = cardWidth * num
        cY = cardHeight * suit
        image = app.cardImage2.crop((cX, cY, 
                                     cX + cardWidth, cY + cardHeight))
        image = app.scaleImage(image, 7/8)
        photoImage = getCachedPhotoImage(app, image)
        canvas.create_image(app.width/2 + index * cardWidth/3, app.height-100,
                            image = photoImage)
        index += 1

def game_drawConsole(app, canvas):
    textX = 128
    textY = 3/4 * app.height
    canvas.create_text(textX, textY, font = "arial 18", text = app.currentMove)
    pass

def game_redrawAll(app, canvas):
    game_drawFelt(app, canvas)
    game_drawBoard(app, canvas)
    game_drawPlayers(app, canvas)
    game_drawConsole(app, canvas)

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

def help_keyPressed(app, event):
    if event.key == "Space":
        app.mode = "pause"

##############
# Main Stuff
##############
def appStarted(app):
    url1 = ("https://s3.amazonaws.com/images.penguinmagic.com/"
            +"images/products/original/8006b.jpg")
    app.cardImage1 = app.loadImage(url1)
    url2 = ("http://www.milefoot.com/math/discrete/counting/images/cards.png")
    app.cardImage2 = app.loadImage(url2)
    app.numberMap = {"Ace":0, "2":1, "3":2, "4":3, "5":4, "6":5, "7":6,
                   "8":7, "9":8, "10":9, "Jack":10, "Queen":11, "King":12}
    app.suitMap = {"Clubs":0, "Spades":1, "Hearts":2, "Diamonds":3}
    app.mode = "splash"
    app.board = [ ]
    app.proceed = False
    app.play = False
    app.turn = 0
    app.stage = app.turn % 3
    app.game = PokerGame()
    app.currentMove = ''

def getCachedPhotoImage(app, image):
    # stores a cached version of the PhotoImage in the PIL/Pillow image
    if ('cachedPhotoImage' not in image.__dict__):
        image.cachedPhotoImage = ImageTk.PhotoImage(image)
    return image.cachedPhotoImage

def playPoker():
    runApp(width=1024, height=512)

def main():
    playPoker()

if __name__ == '__main__':
    main()

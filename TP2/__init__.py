from cmu_112_graphics import *
from Deck import *
from Player import *
import math

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
            if self.players[player].position == 1:
                self.players[player].bet(self.smallBlind)
            elif self.players[player].position == 2:
                self.players[player].bet(self.bigBlind)
        self.currentBet = self.bigBlind

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
        self.gameOver = False
        self.dealt = False
        self.currentBet = 0
        self.pot = 0 

###########
# Start Screen
###########
def splash_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = "dark green")
    canvas.create_text(app.width/2, 30, font = "courier 40", 
                        fill = "light gray",
                        text = "Python Poker")
    canvas.create_rectangle(app.width/2 - 100, app.height/2 - 30, 
                            app.width/2 + 100, app.height/2 + 30,
                            fill = "light gray")
    canvas.create_text(app.width/2, app.height/2, font = "Courier 30",
                        text = "Play")
    canvas.create_rectangle(app.width/2 - 80, app.height/2 + 40, 
                            app.width/2 + 80, app.height/2 + 60,
                            fill = "light gray")
    canvas.create_text(app.width/2, app.height/2+50, font = "Courier 20",
                        text = "Settings")


def splash_keyPressed(app, event):
    app.mode = "game"

def splash_mousePressed(app, event):
    if (event.x <= app.width/2 + 100 and event.x >= app.width/2 - 100 and
    event.y <= app.height/2 + 30 and event.y >= app.height/2 - 30):
        app.mode = "game"
    elif (event.x <= app.width/2 + 80 and event.x >= app.width/2 - 80 and
    event.y <= app.height/2 + 60 and event.y >= app.height/2 + 40):
        app.mode = "settings"

##########
# Game
#########
def game_newPlayer(app, index = 0):
    hand = app.game.dealHand()
    if len(app.game.players) == 0:
        name = "Player 1"
        app.game.addPlayer(Player(hand, len(app.game.players), name))
    else:
        name = Bot.names[index]
        app.game.addPlayer(Bot(hand, len(app.game.players), name))
        index += 1
    
def game_keyPressed(app, event):
    if event.key == "Enter" and not app.play and app.enterPressed:
        app.play = True
        app.game.newRound()
        app.board = [ ]
        app.game.collectBlinds()
        print("hahahahahahhahahahahahah")
    elif event.key == "Enter" and app.play:
        print("here")
    elif event.key == "Enter" and not app.enterPressed:
        app.enterPressed = True
        app.play = True
        app.game.collectBlinds()
    if event.key == "Escape":
        app.mode = "pause"
    if event.key == "Up" and app.upPressed == False:
        app.upPressed = True
        app.start = False
        app.game.dealt = True
        print(app.game.dealt)
        for i in range(8):
            game_newPlayer(app)

def game_mousePressed(app, event):
    buttonSize = 30
    # this huge block of code all checks for button presses for selecting # of
    # players
    if app.start and (event.x <= app.width/2 - 2*buttonSize and 
                      event.x >= app.width/2 - 3*buttonSize and
                      event.y <= app.height/2 + buttonSize and 
                      event.y >= app.height/2 - buttonSize):
        for i in range(2):
            game_newPlayer(app, i-1)
        app.start = False
    elif app.start and (event.x <= app.width/2 - buttonSize and 
                      event.x >= app.width/2 - 2*buttonSize and
                      event.y <= app.height/2 + buttonSize and 
                      event.y >= app.height/2 - buttonSize):
        for i in range(3):
            game_newPlayer(app, i-1)
        app.start = False
    elif app.start and (event.x <= app.width/2 and 
                      event.x >= app.width/2 - buttonSize and
                      event.y <= app.height/2 + buttonSize and 
                      event.y >= app.height/2 - buttonSize):
        for i in range(4):
            game_newPlayer(app, i-1)
        app.start = False
    elif app.start and (event.x <= app.width/2 + buttonSize and 
                      event.x >= app.width/2 and
                      event.y <= app.height/2 + buttonSize and 
                      event.y >= app.height/2 - buttonSize):
        for i in range(5):
            game_newPlayer(app, i-1)
        app.start = False
    elif app.start and (event.x <= app.width/2 + 2 * buttonSize and 
                      event.x >= app.width/2 + buttonSize and
                      event.y <= app.height/2 + buttonSize and 
                      event.y >= app.height/2 - buttonSize):
        for i in range(6):
            game_newPlayer(app, i-1)
        app.start = False
    elif app.start and (event.x <= app.width/2 + 3 * buttonSize and 
                      event.x >= app.width/2 + 2 * buttonSize and
                      event.y <= app.height/2 + buttonSize and 
                      event.y >= app.height/2 - buttonSize):
        for i in range(7):
            game_newPlayer(app, i-1)
        app.start = False
    elif app.start and (event.x <= app.width/2 + 4 * buttonSize and 
                      event.x >= app.width/2 + 3 * buttonSize and
                      event.y <= app.height/2 + buttonSize and 
                      event.y >= app.height/2 - buttonSize):
        for i in range(8):
            game_newPlayer(app, i-1)
        app.start = False

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
    app.game.players[name].played = True

def game_botMove(app, name):
    move = app.game.players[name].playHand(app.board, app.game.pot, 
                                           app.game.currentBet, app.stage) 
    if app.game.currentBet > 0:
        app.game.pot += move[0]
        app.currentMove = move[1]
    else:
        app.currentMove = move[1]
        
        if move[0] > 0:
            if app.game.bet(move[0]) != None:
                game_botMove(app, name)
            else:
                app.game.bet(move[0])
    app.game.players[name].played = True

def game_playStage(app):
    hit = False
    for name in app.game.players:
        if app.game.getNumberPlaying()[0] == 1:
            break
        if (type(app.game.players[name]) == Player and 
            app.game.players[name].playing and
            not app.game.players[name].played):
            game_playerMove(app, name)
            break
        elif (type(app.game.players[name]) == Bot and 
            app.game.players[name].playing and not
            app.game.players[name].played):
            game_botMove(app, name)
            break

    for name in app.game.players:
        if not app.game.players[name].played and app.game.players[name].playing:
            hit = True
    if not hit: # meaning that everyone has played for this round
        app.proceed = True
    return

def game_playPreFlop(app):
    if not app.game.dealt and app.turn > 0:
        for player in app.game.players:
            hand = app.game.dealHand()
            app.game.players[player].hand = hand
        app.game.dealt = True
        return

    if not app.proceed:
        game_playStage(app)
    else:
        app.turn += 1
        app.stage = app.turn % 4
        app.game.nextStage()
        app.board += app.game.dealFlop()
        app.proceed = False

def game_playFlop(app):
    if not app.proceed:
        game_playStage(app)
    else:    
        app.turn += 1
        app.stage = app.turn % 4
        app.game.nextStage()
        app.board.append(app.game.dealTurnOrRiver())
        app.proceed = False

def game_playTurn(app):
    if not app.proceed:
        game_playStage(app)
    else:
        app.turn += 1
        app.stage = app.turn % 4
        app.game.nextStage()
        app.board.append(app.game.dealTurnOrRiver())
        app.proceed = False

def game_playRiver(app):
    if not app.proceed:
        game_playStage(app)
    else:
        winner = app.game.getWinner(app.board)
        print(f"{winner[0]} wins this hand! with {winner[1]}")
        for victor in winner[0]:
            app.game.players[victor].balance += app.game.pot//len(winner[0])
        app.game.removeLosers()
        app.turn += 1
        app.stage = app.turn % 4
        app.play = False
        app.proceed = False
        app.game.nextStage()
        app.currentMove = f"{winner[0]} wins this hand! with {winner[1]}"
def game_timerFired(app):

    print(f"{app.proceed}")
    if app.game.gameOver: 
        app.stage = "gameOver"
        return

    if len(app.game.players) == 1:
        app.game.gameOver = True
        return

    if app.play:
        if app.game.numPlayers > 1 and app.game.getNumberPlaying()[0] == 1:
            player = app.game.getNumberPlaying()[1][0]
            app.game.players[player].balance += app.game.pot
            app.turn += (4-app.stage)
            app.stage = 0
            app.play = False
            app.proceed = False
            return

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
            if app.game.players[name].position == 0:
                game_drawDealerChip(app, canvas, cardAngle, 
                                    centerX, centerY, index)
            elif app.game.players[name].position == 1:
                game_drawSmallBlind(app, canvas, cardAngle,     
                                    centerX, centerY, index)
            elif app.game.players[name].position == 2:
                game_drawBigBlind(app, canvas, cardAngle, 
                                    centerX, centerY, index)

            game_drawBotHand(app, canvas, name, cardAngle, 
                             centerX, centerY, index)
        else:
            if app.game.players[name].position == 0:
                game_drawDealerChip(app, canvas, cardAngle, 
                                    centerX, centerY, index)
            elif app.game.players[name].position == 1:
                game_drawSmallBlind(app, canvas, cardAngle,     
                                    centerX, centerY, index)
            elif app.game.players[name].position == 2:
                game_drawBigBlind(app, canvas, cardAngle, 
                                    centerX, centerY, index)
            game_drawPlayerHand(app, canvas, name)
        index += 1

def game_drawBigBlind(app, canvas, cardAngle, centerX, centerY, index):
    cardAngle += math.pi/4 * index
    numerator = app.width/4 * app.height/4
    denominator = math.sqrt((app.width/4)**2 * math.sin(cardAngle)**2 + 
                                (app.height/4)**2 * math.cos(cardAngle)**2)
    r = numerator/denominator

    blindX = centerX + r * math.cos(cardAngle) - 80
    blindY = centerY + r * math.sin(cardAngle)
    blindR = 40
    canvas.create_oval(blindX, blindY, blindX+blindR, blindY+blindR, 
                        fill = "blue")
    canvas.create_text(blindX + blindR/2, blindY + blindR/2, font = "courier 20",
                        text = "BB")

def game_drawSmallBlind(app, canvas, cardAngle, centerX, centerY, index):
    cardAngle += math.pi/4 * index
    numerator = app.width/4 * app.height/4
    denominator = math.sqrt((app.width/4)**2 * math.sin(cardAngle)**2 + 
                                (app.height/4)**2 * math.cos(cardAngle)**2)
    r = numerator/denominator

    blindX = centerX + r * math.cos(cardAngle) - 80
    blindY = centerY + r * math.sin(cardAngle)
    blindR = 40
    canvas.create_oval(blindX, blindY, blindX+blindR, blindY+blindR, 
                        fill = "white")
    canvas.create_text(blindX + blindR/2, blindY + blindR/2, font = "courier 20",
                        text = "SB")

def game_drawDealerChip(app, canvas, cardAngle, centerX, centerY, index):
    cardAngle += math.pi/4 * index
    numerator = app.width/4 * app.height/4
    denominator = math.sqrt((app.width/4)**2 * (math.sin(cardAngle))**2 + 
                                (app.height/4)**2 * (math.cos(cardAngle)**2))
    r = numerator/denominator

    blindX = centerX + r * math.cos(cardAngle) - 80
    blindY = centerY + r * math.sin(cardAngle)
    blindR = 40
    canvas.create_oval(blindX, blindY, blindX+blindR, blindY+blindR, 
                        fill = "white")
    canvas.create_text(blindX + blindR/2, blindY + blindR/2, font = "courier 10",
                        text = "Dealer")

def game_drawBotHand(app, canvas, name, cardAngle, centerX, centerY, index):
        cardAngle += math.pi/4 * index
        numerator = app.width/4 * app.height/4
        denominator = math.sqrt((app.width/4)**2 * math.sin(cardAngle)**2 + 
                                    (app.height/4)**2 * math.cos(cardAngle)**2)
        r = numerator/denominator
        cardX = centerX + r * math.cos(cardAngle)
        cardY = centerY + r * math.sin(cardAngle)
        nameY = cardY + 40
        chipsY = nameY + 14
        game_drawCard(app, canvas, cardX, cardY)
        canvas.create_text(cardX, chipsY, font = "arial 14 bold",
                        text = f"${app.game.players[name].balance}")
        canvas.create_text(cardX, nameY, font = "arial 14 bold",
                            text = f"{name}")

def game_drawPlayerHand(app, canvas, name):
    index = 0
    cardWidth = 73
    cardHeight = 98
    nameY = app.height-34
    chipsY = app.height - 20

    for card in app.game.players[name].hand:
        num = app.numberMap[card.number]
        suit = app.suitMap[card.suit]
        cX = cardWidth * num
        cY = cardHeight * suit
        image = app.cardImage2.crop((cX, cY, 
                                     cX + cardWidth, cY + cardHeight))
        image = app.scaleImage(image, 7/8)
        photoImage = getCachedPhotoImage(app, image)
        canvas.create_image(app.width/2 + index * cardWidth/3, app.height-100,
                            image = photoImage)
        index += 1
    canvas.create_text(app.width/2, nameY, font = "arial 14 bold",
                       text = name)
    canvas.create_text(app.width/2, chipsY, font = "arial 14 bold",
                       text = f"${app.game.players[name].balance}")

def game_drawConsole(app, canvas):
    print(app.currentMove)
    textX = 128
    textY = 3/4 * app.height
    canvas.create_text(textX, textY, font = "arial 18", text = app.currentMove)

def game_drawPot(app, canvas):
    if app.game.pot == 0:
        return
    else:
        canvas.create_text(app.width/2, app.height * 2/3, 
                           font = "arial 18 bold",
                           text = f"Pot: ${app.game.pot}")

def game_drawStart(app, canvas):
    buttonSize = 30
    canvas.create_text(app.width/2, 30, 
                        font = "Courier 30 bold",
                        fill = "light gray",
                        text = "How many players?")
    for i in range(1,8):
        canvas.create_rectangle(app.width/2 + (i-4) * buttonSize, 
                                app.height/2 - buttonSize,
                                app.width/2 + (i-3) * buttonSize,
                                app.height/2 + buttonSize,
                                fill = "light gray",
                                outline = "black")

        canvas.create_text(app.width/2 + (i-4) * buttonSize + buttonSize/2, 
                            app.height/2, 
                            font = "courier 20 bold",
                            fill = "black",
                            text = f"{i+1}")

def game_redrawAll(app, canvas):
    print("here")
    game_drawFelt(app, canvas)
    game_drawBoard(app, canvas)
    game_drawPlayers(app, canvas)
    game_drawConsole(app, canvas)
    game_drawPot(app, canvas)

    if app.start:
        game_drawStart(app, canvas)
              
    if not app.play and not app.start:
        canvas.create_text(app.width/2, app.height/2, 
                            font = "arial 18 bold",
                            text = "press enter to play!")

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
# gameOver
#############
def gameOver_redrawAll(app, canvas):
    canvas.create_text(app.width/2, app.height/2, font = "Arial 26", 
                        text= "Press enter to play again!")
def gameOver_keyPressed(app, event):
    if event.key == "Enter":
        app.mode = "game"

#############
# settings
#############

def settings_redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill = "dark green")
    canvas.create_text(app.width/2, 20, font = "courier 20",
                        text = "Settings")
    canvas.create_text(app.width/2, 40, font = "courier 14",
                        text = "How many players?")

    canvas.create_rectangle(5,5, 80,30, fill = "light gray")
    canvas.create_text(10, 10, font = "courier 15",
                        text = "<= back", anchor = "nw")

def settings_mousePressed(app, event):
    if (event.x <= 80 and event.x >= 5 and
    event.y <= 30 and event.y >= 5):
        app.mode = "splash"

def settings_keyPressed(app, event):
    pass


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
    app.game = PokerGame(0)
    app.currentMove = ''
    app.upPressed = False
    app.enterPressed = False 
    app.start = True

# from notes
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

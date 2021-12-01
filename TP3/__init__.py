from cmu_112_graphics import *
from Deck import *
from Player import *
from PokerGame import *

import math

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

def splash_mousePressed(app, event):
    if app.numPlayers > 0 and (event.x <= app.width/2 + 100 and 
                               event.x >= app.width/2 - 100 and 
                               event.y <= app.height/2 + 30 and 
                               event.y >= app.height/2 - 30):
        app.mode = "game"
    elif app.numPlayers == 0 and (event.x <= app.width/2 + 100 and 
                               event.x >= app.width/2 - 100 and 
                               event.y <= app.height/2 + 30 and 
                               event.y >= app.height/2 - 30):
        app.mode = "players"
    elif (event.x <= app.width/2 + 80 and event.x >= app.width/2 - 80 and
    event.y <= app.height/2 + 60 and event.y >= app.height/2 + 40):
        app.mode = "settings"

##########
# players
##########

def players_mousePressed(app, event):
    buttonSize = 30
    backX0 = 5
    backY0 = 5
    backX1 = 80
    backY1 = 30
    # this huge block of code all checks for button presses for selecting # of
    # players
    if (event.x <= app.width/2 - 2*buttonSize and 
                      event.x >= app.width/2 - 3*buttonSize and
                      event.y <= app.height/2 + buttonSize and 
                      event.y >= app.height/2 - buttonSize):
        app.numPlayers = 2
        app.mode = "settings"
    elif (event.x <= app.width/2 - buttonSize and 
                      event.x >= app.width/2 - 2*buttonSize and
                      event.y <= app.height/2 + buttonSize and 
                      event.y >= app.height/2 - buttonSize):
        app.numPlayers = 3
        app.mode = "settings"
    elif (event.x <= app.width/2 and 
                      event.x >= app.width/2 - buttonSize and
                      event.y <= app.height/2 + buttonSize and 
                      event.y >= app.height/2 - buttonSize):
        app.numPlayers = 4
        app.mode = "settings"
    elif (event.x <= app.width/2 + buttonSize and 
                      event.x >= app.width/2 and
                      event.y <= app.height/2 + buttonSize and 
                      event.y >= app.height/2 - buttonSize):
        app.numPlayers = 5
        app.mode = "settings"
    elif (event.x <= app.width/2 + 2 * buttonSize and 
                      event.x >= app.width/2 + buttonSize and
                      event.y <= app.height/2 + buttonSize and 
                      event.y >= app.height/2 - buttonSize):
        app.numPlayers = 6
        app.mode = "settings"
    elif (event.x <= app.width/2 + 3 * buttonSize and 
                      event.x >= app.width/2 + 2 * buttonSize and
                      event.y <= app.height/2 + buttonSize and 
                      event.y >= app.height/2 - buttonSize):
        app.numPlayers = 7
        app.mode = "settings"
    elif (event.x <= app.width/2 + 4 * buttonSize and 
                      event.x >= app.width/2 + 3 * buttonSize and
                      event.y <= app.height/2 + buttonSize and 
                      event.y >= app.height/2 - buttonSize):
        app.numPlayers = 8
        app.mode = "settings"

    if (event.x <= backX1 and event.x >= backX0 and
        event.y <= backY1 and event.y >= backY0):
        app.mode = "splash"

def players_drawSelection(app, canvas):
    buttonSize = 30
    canvas.create_text(app.width/2, 30, 
                        font = "Courier 30 bold",
                        fill = "light gray",
                        text = "How many players?")

    for i in range(1,8):
        canvas.create_rectangle(app.width/2 + (i-4.5) * buttonSize, 
                                app.height/2 - buttonSize,
                                app.width/2 + (i-3.5) * buttonSize,
                                app.height/2 + buttonSize,
                                fill = "light gray",
                                outline = "black")

        canvas.create_text(app.width/2 + (i-4.5) * buttonSize + buttonSize/2, 
                            app.height/2, 
                            font = "courier 20 bold",
                            fill = "black",
                            text = f"{i+1}")

def players_redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = "dark green")
    players_drawSelection(app, canvas)
    drawBackButton(app, canvas)

##########
# Game
#########

def game_newPlayer(app, index = 0):
    hand = app.game.dealHand()
    if len(app.game.players) == 0:
        name = app.getUserInput("What is your name?")

        if name == None:
            name = app.getUserInput("Please Re-enter your name")
        if name == None:
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
    elif event.key == "Enter" and app.play:
        return
    elif event.key == "Enter" and not app.enterPressed:
        app.enterPressed = True
        app.play = True
        app.game.collectBlinds()
    if event.key == "Escape":
        app.mode = "pause"

def game_mousePressed(app, event):
    buttonWidth = app.width/20
    buttonHeight = app.height/15
    buttonX0 = app.width - buttonWidth

    if app.isPlayerMove:
        if (event.x >= buttonX0 and event.x <= buttonX0 + buttonWidth and
            event.y > app.height - buttonHeight * 4 and 
            event.y < app.height - buttonHeight * 4 + buttonHeight):
            if app.game.currentBet > 0:
                app.game.players[app.currentPlayer].call(app.game.currentBet)
                app.game.call(app.game.currentBet)
                app.currentMove = (f"{app.currentPlayer} calls")
                app.game.players[app.currentPlayer].played = True
                app.isPlayerMove = False
            else:
                app.game.players[app.currentPlayer].check()
                app.currentMove = f"{app.currentPlayer} checks"
                app.game.players[app.currentPlayer].played = True
            app.isPlayerMove = False
        elif (event.x >= buttonX0 and event.x <= buttonX0 + buttonWidth and 
            event.y > app.height - buttonHeight * 3 and 
            event.y < app.height - buttonHeight * 3 + buttonHeight):
            bet = game_getBet(app)
            if app.game.currentBet > 0:
                app.game.bet(bet)
                app.game.players[app.currentPlayer].bet(bet)
                app.currentMove = (f"{app.currentPlayer} reraises. " +
                                   f"Call {bet} chips to play.")
                app.game.currentBet = bet
                app.game.players[app.currentPlayer].played = True
                app.isPlayerMove = False
            else:
                app.game.bet(bet)
                app.game.players[app.currentPlayer].bet(bet)
                app.currentMove = (f"{app.currentPlayer} puts in {bet} chips.")
                app.game.currentBet = bet
                app.game.players[app.currentPlayer].played = True
                app.isPlayerMove = False
        elif (event.x >= buttonX0 and event.x <= buttonX0 + buttonWidth and
            event.y > app.height - buttonHeight * 2 and 
            event.y < app.height - buttonHeight * 2 + buttonHeight):
            app.game.players[app.currentPlayer].fold()
            app.currentMove = f"{app.currentPlayer} folds." 
            app.game.players[app.currentPlayer].played = True
            app.isPlayerMove = False

def game_getBet(app, invalidInput = False):
    try:
        if invalidInput:
            bet = int(app.getUserInput("Please insert a whole number of dollars."))
            return bet
        else:
            bet = int(app.getUserInput("How much would you like to bet? "
                                        + "(type a number)"))
            return bet
    except ValueError:
        return game_getBet(app, True)

def game_playerMove(app, name):
    app.isPlayerMove = True

def game_botMove(app, name):
    move = app.game.players[name].playHand(app.board, app.game.pot, 
                                           app.game.numPlayers,
                                           app.game.currentBet) 
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

def game_playStage(app, pos):
    hit = False
    for name in app.game.players:
        if app.game.getNumberPlaying()[0] == 1:
            break
        
        if app.game.players[name].position == pos:
            if (type(app.game.players[name]) == Player and 
                app.game.players[name].playing and
                not app.game.players[name].played):
                app.currentPlayer = name
                game_playerMove(app, name)
            elif (type(app.game.players[name]) == Bot and 
                app.game.players[name].playing and not
                app.game.players[name].played):
                app.currentPlayer = name
                game_botMove(app, name)
            break
    
    if app.isPlayerMove:
        return

    for name in app.game.players:
        currPlayer = app.game.players[name]

        if (currPlayer.played and currPlayer.playing and 
            currPlayer.currentBet < app.game.currentBet):
            currPlayer.played = False
            hit = True
        if not currPlayer.played and currPlayer.playing:
            hit = True

    if hit:
        return pos
    else:
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
        if game_playStage(app, app.pos) != None:
            app.pos += 1
        app.pos = app.pos % app.game.numPlayers
        print(app.pos)
    else:
        app.turn += 1
        app.stage = app.turn % 4
        app.game.nextStage()
        app.board += app.game.dealFlop()
        app.proceed = False
        for i in range(app.game.numPlayers):
            tempPos = (app.game.numPlayers - (i + 2)) % app.game.numPlayers
            
            for name in app.game.players:
                currPlayer = app.game.players[name]
                if currPlayer.playing and currPlayer.position == tempPos:
                    app.pos = tempPos
                    return

def game_playFlop(app):
    if not app.proceed:
        if game_playStage(app, app.pos) != None:
            app.pos += 1
        app.pos = app.pos % app.game.numPlayers
    else:    
        app.turn += 1
        app.stage = app.turn % 4
        app.game.nextStage()
        app.board.append(app.game.dealTurnOrRiver())
        app.proceed = False
        for i in range(app.game.numPlayers):
            tempPos = (app.game.numPlayers - (i + 2)) % app.game.numPlayers
            
            for name in app.game.players:
                currPlayer = app.game.players[name]
                if currPlayer.playing and currPlayer.position == tempPos:
                    app.pos = tempPos
                    return

def game_playTurn(app):
    if not app.proceed:
        if game_playStage(app, app.pos) != None:
            app.pos += 1
        app.pos = app.pos % app.game.numPlayers
    else:
        app.turn += 1
        app.stage = app.turn % 4
        app.game.nextStage()
        app.board.append(app.game.dealTurnOrRiver())
        app.proceed = False
        for i in range(app.game.numPlayers):
            tempPos = (app.game.numPlayers - (i + 2)) % app.game.numPlayers
            
            for name in app.game.players:
                currPlayer = app.game.players[name]
                if currPlayer.playing and currPlayer.position == tempPos:
                    app.pos = tempPos
                    return

def game_playRiver(app):
    if not app.proceed:
        if game_playStage(app, app.pos) != None:
            app.pos += 1
        app.pos = app.pos % app.game.numPlayers
    else:
        winner = app.game.getWinner(app.board)
        for victor in winner[0]:
            app.game.players[victor].balance += app.game.pot//len(winner[0])
        app.game.removeLosers()
        app.turn += 1
        app.stage = app.turn % 4
        app.play = False
        app.proceed = False
        app.game.nextStage()
        app.pos = 0
        app.currentMove = f"{winner[0]} wins this hand! with {winner[1]}"

def game_timerFired(app):
    if app.game.gameOver: 
        app.stage = "gameOver"
        return

    if not app.isPlayerMove:
        if app.start:
            for i in range(app.numPlayers):
                game_newPlayer(app, i-1)
            app.start = False

        if len(app.game.players) == 1:
            app.game.gameOver = True
            app.mode = "gameOver"
            return

        if app.play:
            if app.game.numPlayers > 1 and app.game.getNumberPlaying()[0] == 1:
                player = app.game.getNumberPlaying()[1][0]
                app.game.players[player].balance += app.game.pot
                app.currentMove = (f"{app.game.players[player].name} wins this hand! " +
                                    f"with {app.game.players[player].hand}")
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
        folded = False
        if app.game.players[name].position == app.game.numPlayers - 3:
                game_drawDealerChip(app, canvas, cardAngle, 
                                    centerX, centerY, index)
        elif app.game.players[name].position == app.game.numPlayers - 2:
                game_drawSmallBlind(app, canvas, cardAngle,     
                                    centerX, centerY, index)
        elif app.game.players[name].position == app.game.numPlayers - 1:
                game_drawBigBlind(app, canvas, cardAngle, 
                                    centerX, centerY, index)
        if type(app.game.players[name]) == Bot:
            if app.game.players[name].playing:
                game_drawBotHand(app, canvas, name, cardAngle, 
                             centerX, centerY, index)
            else:
                folded = True
                game_drawBotHand(app, canvas, name, cardAngle, 
                             centerX, centerY, index, folded)
        else:
            if app.game.players[name].playing:
                game_drawPlayerHand(app, canvas, name)
            else:
                folded = True
                game_drawPlayerHand(app, canvas, name, folded)
        index += 1

def game_drawBigBlind(app, canvas, cardAngle, centerX, centerY, index):
    cardAngle += math.pi/4 * index
    numerator = app.width/3 * app.height/3
    denominator = math.sqrt((app.width/3)**2 * math.sin(cardAngle)**2 + 
                                (app.height/3)**2 * math.cos(cardAngle)**2)
    r = numerator/denominator

    blindX = centerX + r * math.cos(cardAngle) - 80
    blindY = centerY + r * math.sin(cardAngle)
    blindR = 40
    canvas.create_oval(blindX, blindY, blindX+blindR, blindY+blindR, 
                        fill = "blue")
    canvas.create_text(blindX + blindR/2, blindY + blindR/2, 
                        font = "courier 20 bold",
                        text = "BB")

def game_drawSmallBlind(app, canvas, cardAngle, centerX, centerY, index):
    cardAngle += math.pi/4 * index
    numerator = app.width/3 * app.height/3
    denominator = math.sqrt((app.width/3)**2 * math.sin(cardAngle)**2 + 
                                (app.height/3)**2 * math.cos(cardAngle)**2)
    r = numerator/denominator

    blindX = centerX + r * math.cos(cardAngle) - 80
    blindY = centerY + r * math.sin(cardAngle)
    blindR = 40
    canvas.create_oval(blindX, blindY, blindX+blindR, blindY+blindR, 
                        fill = "white")
    canvas.create_text(blindX + blindR/2, blindY + blindR/2, 
                        font = "courier 20 bold",
                        text = "SB")

def game_drawDealerChip(app, canvas, cardAngle, centerX, centerY, index):
    cardAngle += math.pi/4 * index
    numerator = app.width/3 * app.height/3
    denominator = math.sqrt((app.width/3)**2 * (math.sin(cardAngle))**2 + 
                                (app.height/3)**2 * (math.cos(cardAngle)**2))
    r = numerator/denominator

    blindX = centerX + r * math.cos(cardAngle) - 80
    blindY = centerY + r * math.sin(cardAngle)
    blindR = 40
    canvas.create_oval(blindX, blindY, blindX+blindR, blindY+blindR, 
                        fill = "white")
    canvas.create_text(blindX + blindR/2, blindY + blindR/2, 
                        font = "courier 10 bold",
                        text = "Dealer")

def game_drawBotHand(app, canvas, name, cardAngle, centerX, 
                     centerY, index, folded = False):
        cardAngle += math.pi/4 * index
        numerator = app.width/3 * app.height/3
        denominator = math.sqrt((app.width/3)**2 * math.sin(cardAngle)**2 + 
                                    (app.height/3)**2 * math.cos(cardAngle)**2)
        r = numerator/denominator
        cardX = centerX + r * math.cos(cardAngle)
        cardY = centerY + r * math.sin(cardAngle)
        nameY = cardY + 40
        chipsY = nameY + 14

        if folded:
            canvas.create_text(cardX, cardY, font = "courier 20 bold",
                                text = "Folded")
        else:
            game_drawCard(app, canvas, cardX, cardY)
        canvas.create_text(cardX, chipsY, font = "courier 14 bold",
                        text = f"${app.game.players[name].balance}")
        canvas.create_text(cardX, nameY, font = "courier 14 bold",
                            text = f"{name}")

def game_drawPlayerHand(app, canvas, name, folded = False):
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

        if folded:
            canvas.create_text(app.width/2, app.height - 100, 
                               font = "courier 20 bold",
                               text = "Folded")
            break
        else:
            image = app.cardImage2.crop((cX, cY, 
                                        cX + cardWidth, cY + cardHeight))
            image = app.scaleImage(image, 7/8)
            photoImage = getCachedPhotoImage(app, image)
            canvas.create_image(app.width/2 + index * cardWidth/3, app.height-100,
                                image = photoImage)
        index += 1
    canvas.create_text(app.width/2, nameY, font = "courier 14 bold",
                       text = name)
    canvas.create_text(app.width/2, chipsY, font = "courier 14 bold",
                       text = f"${app.game.players[name].balance}")

def game_drawConsole(app, canvas):

    textX = app.width/2
    textY = app.height/10
    canvas.create_text(textX, textY, font = "courier 18 bold", 
                       text = app.currentMove)

def game_drawPot(app, canvas):
    if app.game.pot == 0:
        return
    else:
        canvas.create_text(app.width/2, app.height * 2/3, 
                           font = "courier 18 bold",
                           text = f"Pot: ${app.game.pot}")

def game_drawCheckButton(app, canvas):
    buttonWidth = app.width/20
    buttonHeight = app.height/15
    buttonX0 = app.width - buttonWidth * 1.1
    buttonY0 = app.height - buttonHeight * 4

    canvas.create_rectangle(buttonX0, buttonY0, buttonX0 + buttonWidth, 
                            buttonY0 + buttonHeight, fill = "light gray",
                            width = 5)
    canvas.create_text(buttonX0 + buttonWidth/2, buttonY0 + buttonHeight/2,
                        font = f"courier 20 bold",
                        text = "Check")

def game_drawCallButton(app, canvas):
    buttonWidth = app.width/20
    buttonHeight = app.height/15
    buttonX0 = app.width - buttonWidth * 1.1
    buttonY0 = app.height - buttonHeight * 4

    canvas.create_rectangle(buttonX0, buttonY0, buttonX0 + buttonWidth, 
                            buttonY0 + buttonHeight, fill = "light gray",
                            width = 5)
    canvas.create_text(buttonX0 + buttonWidth/2, buttonY0 + buttonHeight/2,
                        font = f"courier 20 bold",
                        text = "Call")

def game_drawBetButton(app, canvas):
    buttonWidth = app.width/20
    buttonHeight = app.height/15
    buttonX0 = app.width - buttonWidth * 1.1
    buttonY0 = app.height - buttonHeight * 3

    canvas.create_rectangle(buttonX0, buttonY0, buttonX0 + buttonWidth, 
                            buttonY0 + buttonHeight, fill = "red",
                            width = 5)
    canvas.create_text(buttonX0 + buttonWidth/2, buttonY0 + buttonHeight/2,
                        font = f"courier 20 bold",
                        text = "Bet")

def game_drawFoldButton(app, canvas):
    buttonWidth = app.width/20
    buttonHeight = app.height/15
    buttonX0 = app.width - buttonWidth * 1.1
    buttonY0 = app.height - buttonHeight * 2

    canvas.create_rectangle(buttonX0, buttonY0, buttonX0 + buttonWidth, 
                            buttonY0 + buttonHeight, fill = "Yellow",
                            width = 5)
    canvas.create_text(buttonX0 + buttonWidth/2, buttonY0 + buttonHeight/2,
                        font = f"courier 20 bold",
                        text = "Fold")

def game_drawButtons(app, canvas):
    if app.game.currentBet > 0:
        game_drawCallButton(app, canvas)
    else:
        game_drawCheckButton(app, canvas)
    game_drawBetButton(app, canvas)
    game_drawFoldButton(app, canvas)

def game_redrawAll(app, canvas):
    game_drawFelt(app, canvas)
    game_drawBoard(app, canvas)
    game_drawPlayers(app, canvas)
    game_drawConsole(app, canvas)
    game_drawPot(app, canvas)
    game_drawButtons(app, canvas)
              
    if not app.play and not app.start:
        canvas.create_text(app.width/2, app.height/2, 
                            font = "courier 18 bold",
                            text = "press enter to play!")

###########
# pause
###########

def pause_redrawAll(app, canvas):
    canvas.create_text(app.width/2, app.height/2, font = "courier 26 bold", 
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
    canvas.create_text(app.width/2, 30, fold = "courier 30 bold",
                        text = "Game Over!")
    canvas.create_text(app.width/2, app.height/2, font = "Arial 26", 
                        text= "Return to Main Menu")
def gameOver_keyPressed(app, event):
    if event.key == "Enter":
        app.mode = "game"

#############
# settings
#############

def settings_keyPressed(app, event):
    if event.key == "Escape":
        app.mode = "splash"

def settings_mousePressed(app, event):
    buttonWidth = app.width/10
    buttonHeight = app.height/10
    if (event.x <= 80 and event.x >= 5 and
    event.y <= 30 and event.y >= 5):
        app.mode = "splash"

    if (event.x <= app.width/2 + buttonWidth and 
        event.x >= app.width/2 - buttonWidth and
        event.y <= 40 + 2 * buttonHeight and 
        event.y >= 40 + buttonHeight):
        app.mode = "players"

def settings_drawPlayersButton(app, canvas):
    buttonWidth = app.width/10
    buttonHeight = app.height/10

    canvas.create_rectangle(app.width/2 - buttonWidth, 40 + buttonHeight,
                            app.width/2 + buttonWidth, 40 + 2 * buttonHeight,
                            fill = "light gray")
    canvas.create_text(app.width/2, 40 + 1.5 * buttonHeight, 
                        font = "courier 14", fill = "black",
                        text = "Select Number of Players")

def settings_redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill = "dark green")
    canvas.create_text(app.width/2, 20, font = "courier 30 bold",
                        text = "Settings")
    settings_drawPlayersButton(app, canvas)
    drawBackButton(app, canvas)

def settings_keyPressed(app, event):
    pass

##############
# Main Stuff
##############

def drawBackButton(app, canvas):
    canvas.create_rectangle(5,5, 80,30, fill = "light gray")
    canvas.create_text(10, 10, font = "courier 15",
                        text = "<= back", anchor = "nw")

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
    app.pos = 0
    app.numPlayers = 8
    app.currentPlayer = ""
    app.isPlayerMove = False

# from notes @ https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#cachingPhotoImages
def getCachedPhotoImage(app, image):
    # stores a cached version of the PhotoImage in the PIL/Pillow image
    if ('cachedPhotoImage' not in image.__dict__):
        image.cachedPhotoImage = ImageTk.PhotoImage(image)
    return image.cachedPhotoImage

def playPoker():
    runApp(width=1920, height=1080)

def main():
    playPoker()

if __name__ == '__main__':
    main()

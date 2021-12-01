import random

# playing card is mostly from notes @ https://www.cs.cmu.edu/~112/notes/notes-oop-part3.html#oopyCardsDemo
class PlayingCard:
    numberNames = ["Ace", "2", "3", "4", "5", "6", "7",
                   "8", "9", "10", "Jack", "Queen", "King"]
    suitNames = ["Clubs", "Diamonds", "Hearts", "Spades"]
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
        return f'<{self.number} of {self.suit}>'

# I got heavy inspiration for the hand scoring algo from 
# https://towardsdatascience.com/poker-with-python-how-to-score-all-hands-in-texas-holdem-6fd750ef73d
class Deck:
    numberScoreMap = {"2" : 2, "3" : 3, "4" : 4, "5" : 5, "6" : 6, "7" : 7,
                   "8" : 8, "9" : 9, "10" : 10, "Jack" : 11, "Queen" : 12, 
                   "King" : 13, "Ace" : 14}
    suitMap = {"Clubs" : "c", "Diamonds" : "d", "Hearts" : "h", "Spades" : "s"}
    probabilityMap = {}
    def __init__(self):
        self.deck = self.getDeck()
    
    def __repr__(self):
        return f"Hi This is the deck {self.deck}"
    
    # from notes
    def getDeck(shuffled=True):
        deck = [ ]
        for number in range(0,13):
            for suit in range(0,4):
                numName = PlayingCard.numberNames[number]
                suitName = PlayingCard.suitNames[suit]
                deck.append(PlayingCard(numName, suitName))
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
        return self.getHighCardScore(numbers)

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

    def getHandNumbers(self, hand, board):
        nums = [ self.numberScoreMap[c.number] for c in hand ]
        for card in board:
            num = self.numberScoreMap[card.number]
            nums.append(num)
        
        return nums

    def getHandSuits(self, hand, board):
        suits = [ self.suitMap[c.suit] for c in hand ]
        for card in board:
            suit = self.suitMap[card.suit]
            suits.append(suit)
        
        return suits

    def getNumCounts(self, L):
        counts = dict()

        for num in L:
            counts[L.count(num)] = counts.get(L.count(num), set())
            counts[L.count(num)].add(num)

        return counts

    def getSuitCounts(self, L):
        counts = dict()

        for suit in L:
            counts[L.count(suit)] = counts.get(L.count(suit), set())
            counts[L.count(suit)].add(suit)     

        return counts      

    def calculateHandScore(self, playerHand, board):
        numbers = self.getHandNumbers(playerHand, board)
        suits = self.getHandSuits(playerHand, board)
        numCounts = self.getNumCounts(numbers)
        suitCounts = self.getSuitCounts(suits)
        hand = ""

        if 5 in suitCounts:
            if len(numCounts) == 1 and max(numbers) - min(numbers) == 4:
                hand = "Straight Flush"
                score = self.getStraightFlushScore(numbers)
            else:
                hand = "Flush"
                score = self.getFlushScore(numbers)
        else:
            if 4 in numCounts:
                hand = "Four of a Kind"
                score = self.getQuadsScore(numbers)
            elif 3 in numCounts and 2 in numCounts:
                hand = "Full House"
                score = self.getFullHouseScore(numbers)
            elif len(numCounts) == 1 and max(numbers) - min(numbers) == 4:
                hand = "Straight"
                score = self.getStraightScore(numbers)
            elif 3 in numCounts:
                hand = "Three of a Kind"
                score = self.getThreeOfAKindScore(numbers)
            elif 2 in numCounts and len(numCounts[2]) > 1:
                hand = "Two Pair"
                score = self.getTwoPairScore(numbers)
            elif 2 in numCounts:
                hand = "Pair"
                score = self.getPairScore(numbers)
            else:
                hand = "High Card"
                score = self.getHighCardScore(numbers)

        return (score, hand)
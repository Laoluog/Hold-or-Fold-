import itertools
import random    
from itertools import combinations

class PokerPlayer:
    def __init__(self, name:str):
        self.money = 1000
        self.name = name
        self.bets = []
        self.hand = []
    def place_bet(self, amount: str):
        if int(amount) <= self.money:
            self.bets.append(f"${amount}")
            self.money -= int(amount)
        else:
            print("You do not have enough money to bet that!!")
            print(f"Instead, you will bet your max amount of {self.money}")
            print()
            self.bets.append(f"${self.money}")
            self.money -= int(self.money)
    def get_paid(self):
        newbets = self.bets.copy()
        summ = 0
        for x in range(len(newbets)):
            newbets[x] = newbets[x][1::]
            summ += int(newbets[x])
        self.bets = []
        self.money += 2*summ
    def lose_money(self):
        self.bets = []
    def tied_money(self, amount: str):
        self.bets = []
        self.money += (int(amount))

class PokerGame:
    def __init__(self, p1: str):
        # self.players = [PokerPlayer(p1), PokerPlayer("bot")]
        vals = ['2 of ', '3 of ', '4 of ', '5 of ', '6 of ', '7 of ', '8 of ', '9 of ', '10 of ', 'Jack of ', 'Queen of ', 'King of ', 'Ace of ']
        suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
        
        ## Creating Deck with Itertools Product
        deck = list(itertools.product(vals, suits))
        for i in range(len(deck)):
            deck[i] = "".join(deck[i])

        ## Shuffling Deck and then initializing deck and center cards
        random.shuffle(deck)
        self.deck = deck
        self.allcardspos = self.deck.copy()
        self.cardstoshow = []

    # Deal Hands function
    def deal_hands(self):
        randhand = list(random.sample(self.deck, k=2))

        self.deck.remove(randhand[0])
        self.deck.remove(randhand[1])

        return randhand
    
    # Deals first Three Cards and removes from deck
    def deal_three(self):
        self.cardstoshow = list(random.sample(self.deck, k=3))
        self.deck.remove(self.cardstoshow[0])
        self.deck.remove(self.cardstoshow[1])
        self.deck.remove(self.cardstoshow[2])

    # Deals 4th and 5th Cards and removes from deck, could've been done in one function but this is neater
    def deal_fourth(self):
        self.cardstoshow.append(random.choice(list(self.deck)))
        self.deck.remove(self.cardstoshow[3])
    def deal_fifth(self):
        self.cardstoshow.append(random.choice(list(self.deck)))
        self.deck.remove(self.cardstoshow[4])
    

    # Hardest function, this expresses the value of a function in a list of strings
    def define_hand(self, hand: list, cards: list) -> list:
        # initializing total hand, player hand, dictionaries and lists
        uneditedt = hand + cards
        totallist = hand + cards
        myhand = hand.copy()
        numbsdict = {}
        suitsdict = {}
        handhas = []
        highclist = []

        ## FINDING STRAIGHT
        jazz = totallist.copy()
        for n in range(len(jazz)):
            jazz[n] = jazz[n][0]
        for b in range(len(jazz)):
            if jazz[b] == "A":
                jazz[b] = 14
            elif jazz[b] == "K":
                jazz[b] = 13
            elif jazz[b] == "Q":
                jazz[b] = 12
            elif jazz[b] == "J":
                jazz[b] = 11
        longestt = 0
        leng = 0
        for i in jazz:
            if str(int(i)-1) not in jazz:
                leng = 1
                while str(int(i) + leng) in jazz:
                    leng += 1
                longestt = max(leng, longestt)
        if longestt >= 5:
            handhas.append("Straight")

        # Creating iterable lists of the total hand and player hand
        for x in range(len(totallist)):
            totallist[x] = totallist[x].split(" ")
        for z in range(len(myhand)):
            myhand[z] = myhand[z].split(" ")

        # Creating moving counts of number of matching card types, and then number of matching suits
        for i in totallist:
            if i[0] not in numbsdict:
                numbsdict[i[0]] = 1
            else:
                numbsdict[i[0]] += 1
        for i in totallist:
            if i[2] not in suitsdict:
                suitsdict[i[2]] = 1
            else:
                suitsdict[i[2]] += 1
        zvals = sorted(numbsdict.values())

        # These sort through these dictionaries and assign values to the cards held, utilizing suits and card types
        # Flush
        if max(suitsdict.values()) == 5:
            handhas.append("Flush")
        # Counting Scores(4/3/2/Full House)
        if 4 in zvals:
            value = {i for i in numbsdict if numbsdict[i]== 4}
            handhas.append(f"Four of a Kind of {value}")

        if 3 in zvals:
            nvalue = {i for i in numbsdict if numbsdict[i]== 3}
            handhas.append(f"Three of a Kind of {nvalue}")
        if 3 in zvals and 2 in zvals:
             fvalue = {i for i in numbsdict if numbsdict[i]== 3}
             svalue = {i for i in numbsdict if numbsdict[i]== 2}
             handhas.append(f"Full House of {fvalue} and {svalue}")
        if zvals[-1] == 2 and zvals[-2] == 2:
            gvalue = list({i for i in numbsdict if numbsdict[i]== 2})
            handhas.append(f"Two Pair of {gvalue[0]} and {gvalue[1]}")
        if zvals[-1] == 2:
            dvalue = list({i for i in numbsdict if numbsdict[i]== 2})
            for i in range(len(dvalue)):
                handhas.append(f"Pair of {dvalue[i]}")
        
        ## MUST DO ROYALFLUSH, STRAIGHT FLUSH

        # High Card Check
        for x in range(len(myhand)):
            cardd = myhand[x][0]
            highclist.append(cardd)
        if "Ace" in highclist:
            handhas.append("High Card Ace")
        elif "King" in highclist:
            handhas.append("High Card King")
        elif "Queen" in highclist:
            handhas.append("High Card Queen")
        elif "Jack" in highclist:
            handhas.append("High Card Jack")
        else:
            highclist[0] = int(highclist[0])
            highclist[1] = int(highclist[1])
            highc = max(highclist)
            handhas.append("High Card " + str(highc))
        
        return handhas
    
    ## Scoring every hand based on define_hand, using storage variable to compare value of specific hand on top of its characterizations
    def score_hand(self, hand: list, cards: list):
        fhand = hand.copy()
        checkhand = self.define_hand(fhand, cards)
        storage = [0]*len(checkhand)

        for n in range(len(checkhand)):
            if "Ace" in checkhand[n]:
                storage[n] = 14
            elif "King" in checkhand[n]:
                storage[n] = 13
            elif "Queen" in checkhand[n]:
                storage[n] = 12
            elif "Jack" in checkhand[n]:
                storage[n] = 11
            elif "10" in checkhand[n]:
                storage[n] = 10
            elif "9" in checkhand[n]:
                storage[n] = 9
            elif "8" in checkhand[n]:
                storage[n] = 8
            elif "7" in checkhand[n]:
                storage[n] = 7
            elif "6" in checkhand[n]:
                storage[n] = 6
            elif "5" in checkhand[n]:
                storage[n] = 5
            elif "4" in checkhand[n]:
                storage[n] = 4
            elif "3" in checkhand[n]:
                storage[n] = 3
            else:
                storage[n] = 2

        for i in range(len(checkhand)):
            if "Royal Flush" in checkhand[i]:
                checkhand[i] = 1000 + storage[i]
            elif "Straight Flush" in checkhand[i]:
                checkhand[i] = 900 + storage[i]
            elif "Four of a Kind" in checkhand[i]:
                checkhand[i] = 800 + storage[i]
            elif "Full House" in checkhand[i]:
                checkhand[i] = 700 + storage[i]
            elif "Flush" in checkhand[i]:
                checkhand[i] = 600 + storage[i]
            elif "Straight" in checkhand[i]:
                checkhand[i] = 500 + storage[i]
            elif "Three of a Kind" in checkhand[i]:
                checkhand[i] = 400 + storage[i]
            elif "Two Pair" in checkhand[i]:
                checkhand[i] = 300 + storage[i]
            elif "Pair" in checkhand[i]:
                checkhand[i] = 200 + storage[i]
            elif "High Card" in checkhand[i]:
                checkhand[i] = 100 + storage[i]
        
        checkhand = sorted(checkhand)
        return checkhand

    # Easy enough, just check to see which hand is more valuable
    def winning_hand(self, playhand: list, aihand: list, cards: list) -> str:
         personscore = self.score_hand(playhand, cards)
         aiscore = self.score_hand(aihand, cards)
         if personscore[-1] > aiscore[-1]:
            return "You Won!"
         elif personscore[-1] < aiscore[-1]:
            return "You Lost!"
         else:
            if len(personscore) == 1 or len(aiscore) == 1:
                return "You Tied!"
            elif personscore[-2] > aiscore[-2]:
                return "You Won!"
            elif personscore[-2] < aiscore[-2]:
                return "You Lost!"
            else:
                if len(personscore) == 1 or len(aiscore) == 2:
                    return "You Tied!"
                elif personscore[-3] > aiscore[-3]:
                    return "You Won!"
                elif personscore[-3] < aiscore[-3]:
                    return "You Lost!"
                else:
                    if len(personscore) == 1 or len(aiscore) == 3:
                        return "You Tied!"
                    elif personscore[-4] > aiscore[-4]:
                        return "You Won!"
                    elif personscore[-4] < aiscore[-4]:
                        return "You Lost!"
                    else:
                        return "You Tied!"
                    
    ## Enumerative Check of each and every possibility in the game, split between if the community cards len is 3, 4, or 5
    def get_AI_Enumerative(self, playerdeck: list, centercards: list) -> tuple:
        allpos = self.deck
        ## Must figure out how to check for 5 card
        wins = 0
        loss = 0
        ties = 0
        if len(centercards) == 3:
            newallpos = list(combinations(allpos, 2))
            for i in range(len(newallpos)):
                newallpos[i] = list(newallpos[i])
            centlist = []
            for i in range(len(newallpos)):
                ishlist = []
                ishlist.append(centercards[0])
                ishlist.append(centercards[1])
                ishlist.append(centercards[2])
                ishlist.append(newallpos[i][0])
                ishlist.append(newallpos[i][1])
                centlist.append(ishlist)
            for z in centlist:
                abledeck = allpos
                allotherhands = list(combinations(abledeck, 2))
                for i in range(len(allotherhands)):
                    allotherhands[i] = list(allotherhands[i])
                for x in allotherhands:
                    doeswin = self.winning_hand(playerdeck, x, z)
                    if "Won" in doeswin:
                        wins += 1
                    if "Lost" in doeswin:
                        loss += 1
                    if "Tied" in doeswin:
                        ties += 1
            winp = wins/(wins+loss+ties)
            lossp = loss/(wins+loss+ties)
            tiesp = ties/(wins+loss+ties)
            return (winp, lossp, tiesp)
        elif len(centercards) == 4:
            newallpos = list(combinations(allpos, 1))
            for i in range(len(newallpos)):
                newallpos[i] = list(newallpos[i])
            centlist = []
            for i in range(len(newallpos)):
                ishlist = []
                ishlist.append(centercards[0])
                ishlist.append(centercards[1])
                ishlist.append(centercards[2])
                ishlist.append(centercards[3])
                ishlist.append(newallpos[i][0])
                centlist.append(ishlist)
            for z in centlist:
                abledeck = allpos
                allotherhands = list(combinations(abledeck, 2))
                for i in range(len(allotherhands)):
                    allotherhands[i] = list(allotherhands[i])
                for x in allotherhands:
                    doeswin = self.winning_hand(playerdeck, x, z)
                    if "Won" in doeswin:
                        wins += 1
                    if "Lost" in doeswin:
                        loss += 1
                    if "Tied" in doeswin:
                        ties += 1
            winp = wins/(wins+loss+ties)
            lossp = loss/(wins+loss+ties)
            tiesp = ties/(wins+loss+ties)
            return (winp, lossp, tiesp)
        else:
            newallpos = list(combinations(allpos, 2))
            for i in range(len(newallpos)):
                newallpos[i] = list(newallpos[i])
            for x in newallpos:
                doeswin = self.winning_hand(playerdeck, x, centercards)
                if "Won" in doeswin:
                    wins += 1
                if "Lost" in doeswin:
                    loss += 1
                if "Tied" in doeswin:
                    ties += 1
            winp = wins/(wins+loss+ties)
            lossp = loss/(wins+loss+ties)
            tiesp = ties/(wins+loss+ties)
            return (winp, lossp, tiesp)
        
    # Experimental Check to see percentages of winning, losing, and tying. Runs more efficiently than Enumerative
    def get_AI_Experimental(self, playerdeck: list, centercards: list, trials: int) -> tuple:
        allpos = self.deck
        ## Must figure out how to check for 5 card
        wins = 0
        loss = 0
        ties = 0
        if len(centercards) == 3:
            newallpos = list(combinations(allpos, 2))
            for i in range(len(newallpos)):
                newallpos[i] = list(newallpos[i])
            random.shuffle(newallpos)
            centlist = []
            for i in range(len(newallpos)):
                ishlist = []
                ishlist.append(centercards[0])
                ishlist.append(centercards[1])
                ishlist.append(centercards[2])
                ishlist.append(newallpos[i][0])
                ishlist.append(newallpos[i][1])
                centlist.append(ishlist)
            for z in range(trials):
                abledeck = allpos
                allotherhands = list(combinations(abledeck, 2))
                for i in range(len(allotherhands)):
                    allotherhands[i] = list(allotherhands[i])
                for x in allotherhands:
                    doeswin = self.winning_hand(playerdeck, x, centlist[z])
                    if "Won" in doeswin:
                        wins += 1
                    if "Lost" in doeswin:
                        loss += 1
                    if "Tied" in doeswin:
                        ties += 1
            winp = wins/(wins+loss+ties)
            lossp = loss/(wins+loss+ties)
            tiesp = ties/(wins+loss+ties)
            return (winp, lossp, tiesp)
        elif len(centercards) == 4:
            newallpos = list(combinations(allpos, 1))
            for i in range(len(newallpos)):
                newallpos[i] = list(newallpos[i])
            random.shuffle(newallpos)
            centlist = []
            for i in range(len(newallpos)):
                ishlist = []
                ishlist.append(centercards[0])
                ishlist.append(centercards[1])
                ishlist.append(centercards[2])
                ishlist.append(centercards[3])
                ishlist.append(newallpos[i][0])
                centlist.append(ishlist)
            for z in range(44):
                abledeck = allpos
                allotherhands = list(combinations(abledeck, 2))
                for i in range(len(allotherhands)):
                    allotherhands[i] = list(allotherhands[i])
                for x in allotherhands:
                    doeswin = self.winning_hand(playerdeck, x, centlist[z])
                    if "Won" in doeswin:
                        wins += 1
                    if "Lost" in doeswin:
                        loss += 1
                    if "Tied" in doeswin:
                        ties += 1
            winp = wins/(wins+loss+ties)
            lossp = loss/(wins+loss+ties)
            tiesp = ties/(wins+loss+ties)
            return (winp, lossp, tiesp)
        else:
            newallpos = list(combinations(allpos, 2))
            for i in range(len(newallpos)):
                newallpos[i] = list(newallpos[i])
            for x in newallpos:
                doeswin = self.winning_hand(playerdeck, x, centercards)
                if "Won" in doeswin:
                    wins += 1
                if "Lost" in doeswin:
                    loss += 1
                if "Tied" in doeswin:
                    ties += 1
            winp = wins/(wins+loss+ties)
            lossp = loss/(wins+loss+ties)
            tiesp = ties/(wins+loss+ties)
            return (winp, lossp, tiesp)
        
    # Checker to find (semirandomly) what the AI should bet
    def get_AI_Bet(self, aideck: list, centercards: list, aimoney: int) -> int:
        percents = self.get_AI_Experimental(aideck, centercards, 50)
        recombet = 0
        if percents[0] > 0.5:
            recombet = random.randint((int(aimoney*((percents[0]-0.5)*2))-50), int((aimoney*((percents[0]-0.5)*2))+50))
            if recombet > aimoney:
                recombet = aimoney
        elif percents[0] > 0.25:
            recombet = random.randint(int(aimoney*0.02), int(aimoney*0.1))
        else:
            recombet = random.randint(int(aimoney*0.01), int(aimoney*0.03))
        
        return recombet
    
    # Provides AI recommendations for the amount the user should bet
    def get_AI_Advice(self, percents: tuple, aimoney: int) -> int:
        ourpercents = list(percents)
        recombet = 0
        if ourpercents[0] > 0.5:
            recombet = int(aimoney*((ourpercents[0]-0.5)*2))
            if recombet > aimoney:
                recombet = aimoney
        elif percents[0] > 0.25:
            recombet = int(aimoney*((ourpercents[0]-.20)*0.4))
        else:
            recombet = int(aimoney*0.02)
        
        return recombet
    
    # Should the AI opponent match the bet?
    def will_AI_Match(self, aideck: list, centercards: list, aimoney: int, bet: int) -> bool:
        percents = self.get_AI_Experimental(aideck, centercards, 70)
        if percents[0] > 0.7:
            return True
        elif percents[0] > 0.6 and int(bet)*1.5 < aimoney:
            return True
        elif percents[0] > 0.5 and int(bet)*3 < aimoney:
            return True
        elif percents[0] > 0.4 and int(bet)*4 <= aimoney:
            return True
        elif percents[0] > 0.28 and int(bet)*6 <= aimoney:
            return True
        elif percents[0] > 0.1 and int(bet)*75 <= aimoney:
            return True
        return False
    
    # In the future I want to have the ability to play out multiple hands
    def finish_game(self):
        pass

# EVERYTHING below is terminal display
def runGame():
    print()
    print()
    print()
    print("Hi player! What is your name?")
    # initializing
    p1n = input()
    person = PokerPlayer(p1n)
    aiplayer = PokerPlayer("ai")
    thisgame = PokerGame(p1n)

    # creating hands and starting cards
    person.hand = thisgame.deal_hands()
    aiplayer.hand = thisgame.deal_hands()
    thisgame.deal_three()
    
    def displayScreen():
        print()
        print()
        print()  
        print(f"Player's Name: {person.name}")
        print()
        print()
        print(f"Community Cards: {thisgame.cardstoshow}")
        print()
        print()
        print(f"Your Cards: {person.hand}                                                     Your Money: {person.money} Your Bets: {person.bets}")
        print(f"Your Current Hand: {thisgame.define_hand(person.hand, thisgame.cardstoshow)}")
        print()
        if aineed.lower() == "y" or aineed.lower() == "yes":
            percs = thisgame.get_AI_Experimental(person.hand, thisgame.cardstoshow, 100)
            print(f"You have a win % of: {str(round(percs[0]*100, 2))}%, a loss % of {str(round(percs[1]*100, 2))}%, and a tie % of {str(round(percs[2]*100, 2))}%")
            print(f"The AI recommends that you bet up to or around ${str(round(thisgame.get_AI_Advice(percs, person.money)))}")
            print()
        print(f"AI Player Name: Jacob                                                                            Jacob's Money: {aiplayer.money} Jacob's Bets: {aiplayer.bets}")
        print()

    #First Display Screen
    displayScreen()
    
    print("Would you like to place a bet, check or fold? Please enter (b)et, (c)heck or (f)old")
    willbet = input()
    while willbet.lower() != "b" and willbet.lower() != "bet" and willbet.lower() != "c" and willbet.lower() != "check" and willbet.lower() != "f" and willbet.lower() != "fold":
        print("Please input a valid response:")
        willbet = input() 
    if willbet.lower() == "b" or willbet.lower() == "bet":
        print("How much would you like to bet?")
        amnt = input()
        person.place_bet(amnt)
        if thisgame.will_AI_Match(aiplayer.hand, thisgame.cardstoshow, aiplayer.money, amnt):
            print("The AI will match your bet")
            aiplayer.place_bet(amnt)
        else:
            print("The AI folds")
            person.money = 1000
            aiplayer.lose_money()
            whowon = thisgame.winning_hand(person.hand, aiplayer.hand, thisgame.cardstoshow)
            print(f"Your Opponent's Cards Were: {aiplayer.hand} They Had: {thisgame.define_hand(aiplayer.hand, thisgame.cardstoshow)}")
            if "Won" in whowon:
                print(f"If the game continued, you likely would have won. You now have ${person.money} and AI has ${aiplayer.money}")
            elif "Lost" in whowon:
                print(f"If the game continued, you likely would have lost. You now have ${person.money} and AI has ${aiplayer.money}")
            elif "Tied" in whowon:
                print(f"If the game continued, you likely would have tied. You now have ${person.money} and AI has ${aiplayer.money}")
            quit()
    elif willbet.lower() == "c" or willbet.lower() == "check":
        amnt = thisgame.get_AI_Bet(aiplayer.hand, thisgame.cardstoshow, aiplayer.money)
        print(f"The AI bets ${str(round(amnt))}. Will you match it? Please respond (Y)es or (N)o")
        willmatch = input()
        if willmatch.lower() == "y" or willmatch.lower() == "yes":
            person.place_bet(amnt)
            aiplayer.place_bet(amnt)
        else:
            print("You folded")
            person.money = 1000
            aiplayer.lose_money()
            whowon = thisgame.winning_hand(person.hand, aiplayer.hand, thisgame.cardstoshow)
            print(f"Your Opponent's Cards Were: {aiplayer.hand} They Had: {thisgame.define_hand(aiplayer.hand, thisgame.cardstoshow)}")
            if "Won" in whowon:
                print(f"If the game continued, you likely would have won. You now have ${person.money} and AI has ${aiplayer.money}")
            elif "Lost" in whowon:
                print(f"If the game continued, you likely would have lost. You now have ${person.money} and AI has ${aiplayer.money}")
            elif "Tied" in whowon:
                print(f"If the game continued, you likely would have tied. You now have ${person.money} and AI has ${aiplayer.money}")
            quit()
    elif willbet.lower() == "f" or willbet.lower() == "fold":
        print("You folded")
        person.money = 1000
        aiplayer.lose_money()
        whowon = thisgame.winning_hand(person.hand, aiplayer.hand, thisgame.cardstoshow)
        print(f"Your Opponent's Cards Were: {aiplayer.hand} They Had: {thisgame.define_hand(aiplayer.hand, thisgame.cardstoshow)}")
        if "Won" in whowon:
            print(f"If the game continued, you likely would have won. You now have ${person.money} and AI has ${aiplayer.money}")
        elif "Lost" in whowon:
            print(f"If the game continued, you likely would have lost. You now have ${person.money} and AI has ${aiplayer.money}")
        elif "Tied" in whowon:
            print(f"If the game continued, you likely would have tied. You now have ${person.money} and AI has ${aiplayer.money}")
        quit()        



            
            
    ## MUST INTRODUCE AI BETS WITH CHECKS, AND WHAT HAPPENS IF I FOLD
    # Here is where I introduce the bot! AND I'll put AI advice here
    

    #Fourth Card Dealt
    thisgame.deal_fourth()
    displayScreen()

    print("Would you like to place a bet, check or fold? Please enter (b)et, (c)heck or (f)old")
    willbet2 = input()
    while willbet2.lower() != "b" and willbet2.lower() != "bet" and willbet2.lower() != "c" and willbet2.lower() != "check" and willbet2.lower() != "f" and willbet2.lower() != "fold":
        print("Please input a valid response:")
        willbet2 = input() 
    if willbet2.lower() == "b" or willbet2.lower() == "bet":
        print("How much would you like to bet?")
        amnt2 = input()
        if thisgame.will_AI_Match(aiplayer.hand, thisgame.cardstoshow, aiplayer.money, amnt2):
            print("The AI will match your bet")
            person.place_bet(amnt2)
            aiplayer.place_bet(amnt2)
        else:
            print("The AI folds")
            person.get_paid()
            aiplayer.lose_money()
            whowon = thisgame.winning_hand(person.hand, aiplayer.hand, thisgame.cardstoshow)
            print(f"Your Opponent's Cards Were: {aiplayer.hand} They Had: {thisgame.define_hand(aiplayer.hand, thisgame.cardstoshow)}")
            if "Won" in whowon:
                print(f"If the game continued, you likely would have won. You now have ${person.money} and AI has ${aiplayer.money}")
            elif "Lost" in whowon:
                print(f"If the game continued, you likely would have lost. You now have ${person.money} and AI has ${aiplayer.money}")
            elif "Tied" in whowon:
                print(f"If the game continued, you likely would have tied. You now have ${person.money} and AI has ${aiplayer.money}")
            quit()
    elif willbet2.lower() == "c" or willbet2.lower() == "check":
        amnt2 = thisgame.get_AI_Bet(aiplayer.hand, thisgame.cardstoshow, aiplayer.money)
        print(f"The AI bets ${str(round(amnt2))}. Will you match it? Please respond (Y)es or (N)o")
        willmatch = input()
        if willmatch.lower() == "y" or willmatch.lower() == "yes":
            person.place_bet(amnt2)
            aiplayer.place_bet(amnt2)
        else:
            print("You folded")
            person.lose_money()
            aiplayer.get_paid()
            whowon = thisgame.winning_hand(person.hand, aiplayer.hand, thisgame.cardstoshow)
            print(f"Your Opponent's Cards Were: {aiplayer.hand} They Had: {thisgame.define_hand(aiplayer.hand, thisgame.cardstoshow)}")
            if "Won" in whowon:
                print(f"If the game continued, you likely would have won. You now have ${person.money} and AI has ${aiplayer.money}")
            elif "Lost" in whowon:
                print(f"If the game continued, you likely would have lost. You now have ${person.money} and AI has ${aiplayer.money}")
            elif "Tied" in whowon:
                print(f"If the game continued, you likely would have tied. You now have ${person.money} and AI has ${aiplayer.money}")
            quit()
    elif willbet2.lower() == "f" or willbet2.lower() == "fold":
        print("You folded")
        person.lose_money()
        aiplayer.get_paid()
        whowon = thisgame.winning_hand(person.hand, aiplayer.hand, thisgame.cardstoshow)
        print(f"Your Opponent's Cards Were: {aiplayer.hand} They Had: {thisgame.define_hand(aiplayer.hand, thisgame.cardstoshow)}")
        if "Won" in whowon:
            print(f"If the game continued, you likely would have won. You now have ${person.money} and AI has ${aiplayer.money}")
        elif "Lost" in whowon:
            print(f"If the game continued, you likely would have lost. You now have ${person.money} and AI has ${aiplayer.money}")
        elif "Tied" in whowon:
            print(f"If the game continued, you likely would have tied. You now have ${person.money} and AI has ${aiplayer.money}")
        quit()

    #Fifth Card Dealt
    thisgame.deal_fifth()
    displayScreen()

    print("Would you like to place a bet, check or fold? Please enter (b)et, (c)heck or (f)old")
    willbet3 = input()
    while willbet3.lower() != "b" and willbet3.lower() != "bet" and willbet3.lower() != "c" and willbet3.lower() != "check" and willbet3.lower() != "f" and willbet3.lower() != "fold":
        print("Please input a valid response:")
        willbet3 = input() 
    if willbet3.lower() == "b" or willbet3.lower() == "bet":
        print("How much would you like to bet?")
        amnt3 = input()
        if thisgame.will_AI_Match(aiplayer.hand, thisgame.cardstoshow, aiplayer.money, amnt3):
            print("The AI will match your bet")
            person.place_bet(amnt3)
            aiplayer.place_bet(amnt3)
        else:
            print("The AI folds")
            person.get_paid()
            aiplayer.lose_money()
            whowon = thisgame.winning_hand(person.hand, aiplayer.hand, thisgame.cardstoshow)
            print(f"Your Opponent's Cards Were: {aiplayer.hand} They Had: {thisgame.define_hand(aiplayer.hand, thisgame.cardstoshow)}")
            if "Won" in whowon:
                print(f"If the game continued, you likely would have won. You now have ${person.money} and AI has ${aiplayer.money}")
            elif "Lost" in whowon:
                print(f"If the game continued, you likely would have lost. You now have ${person.money} and AI has ${aiplayer.money}")
            elif "Tied" in whowon:
                print(f"If the game continued, you likely would have tied. You now have ${person.money} and AI has ${aiplayer.money}")
            quit()
    elif willbet3.lower() == "c" or willbet3.lower() == "check":
        amnt3 = thisgame.get_AI_Bet(aiplayer.hand, thisgame.cardstoshow, aiplayer.money)
        print(f"The AI bets ${str(round(amnt3))}. Will you match it? Please respond (Y)es or (N)o")
        willmatch = input()
        if willmatch.lower() == "y" or willmatch.lower() == "yes":
            person.place_bet(amnt3)
            aiplayer.place_bet(amnt3)
        else:
            print("You folded")
            aiplayer.get_paid()
            person.lose_money()
            whowon = thisgame.winning_hand(person.hand, aiplayer.hand, thisgame.cardstoshow)
            print(f"Your Opponent's Cards Were: {aiplayer.hand} They Had: {thisgame.define_hand(aiplayer.hand, thisgame.cardstoshow)}")
            if "Won" in whowon:
                print(f"If the game continued, you likely would have won. You now have ${person.money} and AI has ${aiplayer.money}")
            elif "Lost" in whowon:
                print(f"If the game continued, you likely would have lost. You now have ${person.money} and AI has ${aiplayer.money}")
            elif "Tied" in whowon:
                print(f"If the game continued, you likely would have tied. You now have ${person.money} and AI has ${aiplayer.money}")
            quit()
    elif willbet3.lower() == "f" or willbet3.lower() == "fold":
        print("You folded")
        person.lose_money()
        aiplayer.get_paid()
        whowon = thisgame.winning_hand(person.hand, aiplayer.hand, thisgame.cardstoshow)
        print(f"Your Opponent's Cards Were: {aiplayer.hand} They Had: {thisgame.define_hand(aiplayer.hand, thisgame.cardstoshow)}")
        if "Won" in whowon:
            print(f"If the game continued, you likely would have won. You now have ${person.money} and AI has ${aiplayer.money}")
        elif "Lost" in whowon:
            print(f"If the game continued, you likely would have lost. You now have ${person.money} and AI has ${aiplayer.money}")
        elif "Tied" in whowon:
            print(f"If the game continued, you likely would have tied. You now have ${person.money} and AI has ${aiplayer.money}")
        quit()

    #Final Results
    displayScreen()

    print(f"You Had: {thisgame.define_hand(person.hand, thisgame.cardstoshow)}")
    print()
    print(f"Your Opponent's Cards Were: {aiplayer.hand} They Had: {thisgame.define_hand(aiplayer.hand, thisgame.cardstoshow)}")
    whowon = thisgame.winning_hand(person.hand, aiplayer.hand, thisgame.cardstoshow)
    if "Won" in whowon:
        person.get_paid()
        aiplayer.lose_money
    if "Lost" in whowon:
        aiplayer.get_paid()
        person.lose_money()
    if "Tied" in whowon:
        person.tied_money(str(int(amnt) + int(amnt2) + int(amnt3)))
        aiplayer.tied_money(str(int(amnt) + int(amnt2) + int(amnt3)))
    print(f"{whowon}! You now have ${person.money} and AI has ${aiplayer.money}")
if __name__ == "__main__":
    print()
    print()
    print()
    print()
    print()
    print("Hi! Before we start this Poker Game, do you need instructions on how to play? Please respond (Y)es or (N)o")
    instr = input()
    while instr.lower() != "y" and instr.lower() != "yes" and instr.lower() != "n" and instr.lower() != "no":
        print("Please input a valid response:")
        instr = input() 
    if instr.lower() == "y" or instr.lower() == "yes":
        print()
        print("Poker Instructions:")
        print("All players are dealt 2 cards face down, followed by 5 cards face up. Players must make the best possible 5 card poker hand using the 5 community cards and their own face down hole cards. The best 5 card poker hand wins the hand and receives the pot.")
        print("At various stages players bet against each other on the value of their hands. A player can fold their hand at any stage.")
        print("Each betting stage is identical, and there are 4 stages of betting as listed below. They have fancy names but don't let it confuse you, you can think of them as stages 1-4. Once the betting stage is resolved, the next stage of the hand starts.")
        print("If you need more in depth rules on how to play, or you would like to see the hand chart, please visit:")
        print()
        print("https://upswingpoker.com/poker-rules/")
        print()
        print()
        print("Would you like AI-Powered Advice during this game? Please respond (Y)es or (N)o")
        aineed = input()
        while aineed.lower() != "y" and aineed.lower() != "yes" and aineed.lower() != "n" and aineed.lower() != "no":
            print("Please input a valid response:")
            aineed = input() 
        runGame()
    else:
        print("Would you like AI-Powered Advice during this game? Please respond (Y)es or (N)o")
        aineed = input()
        while aineed.lower() != "y" and aineed.lower() != "yes" and aineed.lower() != "n" and aineed.lower() != "no":
            print("Please input a valid response:")
            aineed = input() 
        runGame()

    # print(person.hand, aiplayer.hand, thisgame.cardstoshow)
    # thisgame.define_hand(person.hand, thisgame.cardstoshow)
    # thisgame.winning_hand(person.hand, aiplayer.hand, thisgame.cardstoshow)

#AHHHHHH HAVE TO FIGURE OUT CLASSES
import sys
from cards import *
from player import *
import itertools
SMALLBLIND = 50
BIGBLIND = 100
total = {}
potPool = 0
turn = False
river = False 
prevChoice = [] #use to figure out if someone bet or raised
def find_winner():
    """Find and announce the winner."""
    for position, player in total.items():
        if player.folded:
            continue  # skip folded players
        best_hand_value = None
        best_hand = None
        # Get all combinations of 5 cards out of the player's hand and the board
        for combination in itertools.combinations(player.hand + board, 5):
            value = hand_value(list(combination))
            if best_hand_value is None or value > best_hand_value:
                best_hand_value = value
                best_hand = combination
        player.best_hand_value = best_hand_value
        player.best_hand = best_hand

    # Find the player(s) with the best hand
    winners = [player for position, player in total.items() if player.best_hand_value == max(player.best_hand_value for player in total.values())]
    for winner in winners:
        print("{} wins with hand: {}".format(winner.name, winner.best_hand))
def commands(player):
    global potPool
    choice = input('''
    (C)heck
    (R)aise
    (B)et
    (F)old
    ''')

    if player.folded == True:
        pass
    elif "C" == choice or "c" == choice:
        print("{} choose to check".format(player.name))
        pass
    elif choice == 'R' or choice == 'r':
        print("{} choose to check".format(player.name))
        amount = input("Enter how much you would like to raise: ")
        player.reduceBalance(int(amount))
        #TODO might be better to have function retrieve pot amount
        #TODO logic for minimum amount to raise
        potPool=potPool+int(amount)
        print("Pot: {}".format(potPool))
    elif choice == 'B' or choice == 'b':
        print("{} choose to bet".format(player.name))
        amount = input("Enter how much you would like to bet: ")
        player.reduceBalance(int(amount))
        #TODO might be better to have function retrieve pot amount
        #TODO logic for minimum amount to be
        potPool=potPool+int(amount)
        print("Pot: {}".format(potPool))
    elif choice == 'F' or choice == 'f':
            print("{} choose to fold".format(player.name))
            player.folded=True
    else:
        print("ERROR: Not a valid choice")
    return choice

def start():
    print('Welcome to Texas Holdem!')
    while True:
        count=int(input('How many players are playing today: '))
        if count<=9 and count>0:
            for i in range(count):
                name=input("Enter player name: ")
                total[i]= Player(name,1000,[],False)
            break
        elif count<=0:
            print("You need have more than one player to play")
            continue
        elif count>9:
            print("You have to many players to play")
            continue
        else:
            print("ERROR: You didnt input a number")
            continue

def acction(command):
    global prevChoice
    while True:
        if command == "b" or command == "B" in prevChoice:
            print("You have to call the previous bet")
        elif command == "r" or command == "R" in prevChoice:
            print("You have to call the previous raise")
            

def main():
    start()

if __name__ == '__main__':
    main()
    deck = getDeck()
    round = -1
    for i in range(len(total)):
        for j in range(2):
            total[i].hand.append(deck.pop())
    discard=[deck.pop()]
    board=[deck.pop(),deck.pop(),deck.pop()]
    while True:

        for position, player in total.items(): 
            #makes an orbit
            #use a modulus to determine who is what position to
            # big blind, small blind, dealer, etc...
            if position == 0:
                round += 1
            if round == 0:
                print("{} hand".format(player.name))
                displayHands(player.hand)
                prevChoice.append(commands(player))

            elif round == 1:
                #flop
                print("Board")
                displayHands(board)
                if player.folded:
                    pass
                else:
                    print("{} hand".format(player.name))
                    displayHands(player.hand)
                    commands(player)
            elif round == 2:
                #turn
                if turn == False:
                    #have not seen the turn yet
                    discard.append(deck.pop())
                    board.append(deck.pop())
                    turn = True
                    #now have we have seen the turn
                print("Board")
                displayHands(board)
                if player.folded:
                    pass
                else:
                    print("{} hand".format(player.name))
                    displayHands(player.hand)
                    commands(player)
            elif round == 3:
                #river
                if river == False:
                    #have not seen the river yet
                    discard.append(deck.pop())
                    board.append(deck.pop())
                    river = True
                    #now we have seen the river 
                  
                print("Board")
                displayHands(board)
                if player.folded:
                    pass
                else:
                    print("{} hand".format(player.name))
                    displayHands(player.hand)
                    commands(player)
            elif round < 4:
                round += 1
            else:
                find_winner()
                sys.exit()


        

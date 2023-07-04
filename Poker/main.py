import sys
from cards import *
from player import *
import itertools
SMALLBLIND = 50
BIGBLIND = 100
total = {}
potPool = 0
turn = False
last_bet = 0
river = False 
prevChoice = [] #use to figure out if someone bet or raised
prevAmount = [] #use to figure out previous bet amount
board = []

def get_pot_amount():
    """Return the current pot amount."""
    return potPool

def minimum_bet():
    """Determine the minimum bet amount."""
    if len(prevAmount) == 0:
        return BIGBLIND  # if no previous bet, minimum bet is BIGBLIND
    return max(prevAmount)  # otherwise, minimum bet is the maximum of the previous bets

def minimum_raise():
    """Determine the minimum raise amount."""
    if len(prevAmount) == 0:
        return 2 * BIGBLIND  # if no previous bet, minimum raise is 2*BIGBLIND
    return max(prevAmount) + BIGBLIND  # otherwise, minimum raise is maximum of previous bets + BIGBLIND


def find_winner():
    """Find and announce the winner."""
    for position, player in total.items():
        if player.folded:
            continue  # skip folded players
        assert isinstance(player.hand, list), "player.hand must be a list"
        assert isinstance(board, list), "board must be a list"
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
    global total
    global prevChoice
    global prevAmount
    global last_bet

    if player.folded:
        return

    print("The minimum bet amount is {0}".format(minimum_bet()))

    if last_bet > 0:
        print("The last bet was {0}. You must bet this amount or fold.".format(last_bet))

    while True:
        choice = input('''
        (C)heck
        (R)aise
        (B)et
        (F)old
        ''').lower()

        if choice == 'c':
            if last_bet > 0:
                print("You must match the last bet or fold.")
                continue  # Continue the loop to allow the player to choose a valid command
            else:
                print("{} choose to check".format(player.name))
                break
        elif choice == 'r':
            amount = input("Enter how much you would like to raise: ")
            amount = int(amount)
            if amount >= minimum_raise():
                player.reduceBalance(amount)
                potPool += amount
                last_bet = amount
                print("{} choose to raise. Pot: {}".format(player.name, potPool))
                break
            else:
                print("Can't raise that amount")
        elif choice == 'b':
            amount = input("Enter how much you would like to bet: ")
            amount = int(amount)
            if (last_bet > 0 and amount == last_bet) or (last_bet == 0 and amount >= minimum_bet()):
                player.reduceBalance(amount)
                player.bet += amount  # update the player's current bet
                potPool += amount
                last_bet = amount
                print("{} choose to bet. Pot: {}".format(player.name, potPool))
                break
        elif choice == 'f':
            print("{} choose to fold".format(player.name))
            player.folded=True
            break
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


def main():
    global turn
    global river
    global board
    while True:  # This loop represents each game
        turn = False
        river = False
        start()
        deck = getDeck()
        for i in range(len(total)):
            total[i].hand = [deck.pop(), deck.pop()]
        discard = [deck.pop()]
        board = [deck.pop(), deck.pop(), deck.pop()]

        for round in range(4):  # This loop represents each betting round in a game
            bet_placed = False
            player_index = 0
            while True:
                player = total[player_index]
                if player.folded:
                    player_index = (player_index + 1) % len(total)
                    if player_index == 0 and not bet_placed:  # Check if we've gone full circle without a new bet
                        break
                    continue
                if round == 0:
                    print("{}'s hand:".format(player.name))
                    displayHands(player.hand)
                else:
                    if round == 1:
                        round_name = "Flop"
                    elif round == 2:
                        if not turn:
                            board.append(deck.pop())
                            turn = True
                        round_name = "Turn"
                    else:  # round == 3
                        if not river:
                            board.append(deck.pop())
                            river = True
                        round_name = "River"
                    print("\n{}\nBoard:".format(round_name))
                    displayHands(board)
                    print("{}'s hand:".format(player.name))
                    displayHands(player.hand)
                command = commands(player)
                player_index = (player_index + 1) % len(total)
                if command in {'b', 'r'}:  # If player bets or raises, we'll need to keep going until no new bets
                    bet_placed = True
                elif player_index == 0 and not bet_placed:  # Check if we've gone full circle without a new bet
                    break

        # Determine the winner among players who haven't folded
        find_winner()

if __name__ == '__main__':
    main()
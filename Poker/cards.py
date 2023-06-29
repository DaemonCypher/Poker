import random
from player import*
# Set up the constants:
HEARTS   = chr(9829) # Character 9829 is '♥'.
DIAMONDS = chr(9830) # Character 9830 is '♦'.
SPADES   = chr(9824) # Character 9824 is '♠'.
CLUBS    = chr(9827) # Character 9827 is '♣'.
BACKSIDE = 'backside'
def getDeck():
    """Return a list of (rank, suit) tuples for all 52 cards."""
    deck = []
    for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))  # Add the numbered cards.
        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))  # Add the face and ace cards.
    random.shuffle(deck)
    return deck
def displayHands(cards):
    """Show the player's and dealer's cards. Hide the dealer's first
    card if showDealerHand is False."""
    print()
    displayCards(cards)

def displayCards(cards):
    """Display all the cards in the cards list."""
    rows = ['', '', '', '', '']  # The text to display on each row.

    for i, card in enumerate(cards):
        rows[0] += ' ___  '  # Print the top line of the card.
        if card == BACKSIDE:
            # Print a card's back:
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            # Print the card's front:
            rank, suit = card  # The card is a tuple data structure.
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))
    for row in rows:
        print(row)
        
    # Print each row on the screen:
    # The card ranks from lowest to highest
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def hand_value(hand):
    """Calculate and return the value of the hand."""
    # Each function checks for a specific poker hand. The order in
    # which they are checked is important, since higher value hands
    # should be checked first.
    functions = [is_royal_flush, is_straight_flush, is_four_of_a_kind,
                 is_full_house, is_flush, is_straight, is_three_of_a_kind,
                 is_two_pair, is_pair, is_high_card]
    for i, function in enumerate(functions):
        result = function(hand)
        if result:
            return len(functions) - i, result  # Return ranking and cards
    return None

def is_royal_flush(hand):
    if is_flush(hand) and is_straight(hand) and sorted(hand)[4][0] == 'A':
        return sorted(hand, key=lambda x: RANKS.index(x[0]))
    return False

def is_straight_flush(hand):
    if is_flush(hand) and is_straight(hand):
        return sorted(hand, key=lambda x: RANKS.index(x[0]))
    return False

def is_four_of_a_kind(hand):
    ranks = [card[0] for card in hand]
    for rank in ranks:
        if ranks.count(rank) == 4:
            return sorted(hand, key=lambda x: (ranks.count(x[0]), RANKS.index(x[0])), reverse=True)
    return False

def is_flush(hand):
    suits = [card[1] for card in hand]
    if len(set(suits)) == 1:
        return True
    return False

def is_straight(hand):
    ranks = [RANKS.index(card[0]) for card in hand]
    ranks.sort()
    if len(set(ranks)) == 5 and (ranks[4] - ranks[0] == 4):
        return True
    return False

def is_full_house(hand):
    ranks = [card[0] for card in hand]
    rank_counts = [ranks.count(rank) for rank in ranks]
    if set(rank_counts) == {2, 3}:
        return True
    return False

def is_three_of_a_kind(hand):
    ranks = [card[0] for card in hand]
    rank_counts = [ranks.count(rank) for rank in ranks]
    if 3 in rank_counts:
        return True
    return False

def is_two_pair(hand):
    ranks = [card[0] for card in hand]
    rank_counts = [ranks.count(rank) for rank in ranks]
    if list(sorted(rank_counts)).count(2) == 4:
        return True
    return False

def is_pair(hand):
    ranks = [card[0] for card in hand]
    rank_counts = [ranks.count(rank) for rank in ranks]
    if 2 in rank_counts:
        return True
    return False

def is_high_card(hand):
    ranks = [RANKS.index(card[0]) for card in hand]
    if len(set(ranks)) == 5:
        return True
    return False

def compare_hands(player_hand, dealer_hand):
    player_value = hand_value(player_hand)
    dealer_value = hand_value(dealer_hand)

    if player_value and dealer_value:
        if player_value > dealer_value:
            return 'player'
        elif dealer_value > player_value:
            return 'dealer'
        else:
            return 'tie'
    else:
        return 'error'  # Return 'error' if hand_value returned None

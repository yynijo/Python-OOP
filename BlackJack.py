import random

suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
             'Queen':10, 'King':10, 'Ace':11}

class Card:
    def __init__(self, suit: str, rank:str) -> None:
        self.suit: str = suit
        self.rank: str = rank
    
    def __str__(self) -> str:
        return (f'{self.rank} of {self.suit}')
    
class Deck:
    def __init__(self) -> None:
        self.deck: list = []  # Start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self) -> str:
        deck_comp = ''         # Start with empty string
        for card in self.deck: # Concat every card in deck to string
            deck_comp += '\n' + card.__str__()
        return (f"This deck has: {deck_comp}")

    def shuffle(self) -> None: 
        random.shuffle(self.deck)
        
    def deal(self) -> str:
        return self.deck.pop() # Last card appended is the first card drawn

class Hand:
    def __init__(self) -> None:
        self.cards: list = [] 
        self.value: int = 0 # Total value of hand
        self.aces: int = 0  # Number of aces
    
    def add_card(self, card: str) -> None:
        self.cards.append(card)
        self.value += values[card.rank] 

        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self) -> None:
        if self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1  # Minus ace for __

class Chips:
    def __init__(self) -> None:
        self.total: int = 100 
        self.bet: int = 0
        
    def win_bet(self) -> None:
        self.total += 2* self.bet
    
    def lose_bet(self) -> None:
        self.total -= self.bet

def take_bet(chips: Chips) -> None:
    ''' Function to let player take a bet. Takes in Chips object from each player '''
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet"))
        except ValueError: # Not valid string representation of integer
            print("Your input must be an integer")
        else:
            if chips.bet > chips.total:
                print(f"Sorry, your bet can't exceed {chips.total}")
            else:
                break

def hit(deck: Deck, hand: Hand) -> None:
    '''Function to let player take a hit from the dealer. Takes in Deck and Hand objects'''
    hand.add_card(deck.deal())
    hand.adjust_for_ace()
    
def hit_or_stand(deck: Deck, hand: Hand) -> None:
    ''' Function to let player choose whether to hit or stand, then execute functions. Uses if-elif-else for input checking'''
    global playing 
    while True:
        x = input("Dealer: Would you like to hit or stand? Enter h or s.").lower()
        if x[0] == 'h':
            print("You have chosen to hit!")
            hit(deck,hand)
            break
        elif x[0] == 's':
            print("You have chosen to stand!")
            playing = False
            break
        else:
            print("Sorry, please try again")

def show_some(player: Hand ,dealer: Hand) -> None:
    '''Take in player's and dealer's Hand object to display all of player's cards and only 1 of Dealer's card'''
    your_hand_str = ', '.join([str(i) for i in player.cards])

    print(f'Your hand is {your_hand_str}. The total value is {player.value}')
    print(f'The dealers first card is {dealer.cards[0]}')
    
def show_all(player: Hand, dealer: Hand) -> None:
    your_hand_str = ', '.join([str(i) for i in player.cards])
    dealer_hand_str = ', '.join([str(i) for i in Thedealer.cards])

    print(f'Your hand is {your_hand_str}. The total value is {player.value}')
    print(f'The dealers hand is {dealer_hand_str}. The total value is {dealer.value}')

def player_busts(chips: Chips) -> None:
    print("You bust!")
    chips.lose_bet()

def player_wins(chips: Chips) -> None:
    print("You win!")
    chips.win_bet()

def dealer_busts(chips: Chips) -> None:
    print("The dealer busts!")
    chips.win_bet()
    
def dealer_wins(chips: Chips) -> None:
    print("The dealer wins!")
    chips.lose_bet()
    
def push() -> None:
    print("Dealer & player tie!")

while True:
    # Print an opening statement
    print("Welcome to Blackjack! Get as close to 21 as you can without going over!")
    print("Dealer hits until she reaches 17. Aces count as 1 or 11.\n")

    play_game = input("Are you ready to play? Enter Yes or No: ").lower()
    if play_game[0] == 'y':
        playing = True
    else:
        print("Thanks for stopping by! Goodbye!")
        break
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    player_1, Thedealer = Hand(), Hand()

    player_1.add_card(deck.deal())
    player_1.add_card(deck.deal())
    Thedealer.add_card(deck.deal())
    Thedealer.add_card(deck.deal())
            
    # Set up the Player's chips (First time only)
    if 'player_1_chips' not in locals():
        player_1_chips = Chips()
    
    # Prompt the Player for their bet
    take_bet(player_1_chips)
    
    # Keep 1 dealer card hidden
    print('A new round starts!\n')
    show_some(player_1,Thedealer)
    
    while playing:  # From hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_1)
        
        # Show cards (but keep one dealer card hidden)
        print('\nYour hand is now:')
        show_some(player_1,Thedealer)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_1.value > 21:
            player_busts(player_1_chips)
            break
        
    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_1.value <= 21:
        while Thedealer.value < 17:
            hit(deck,Thedealer)

        # Show all cards
        print('\nThe final board for this round is:')
        show_all(player_1,Thedealer)
        print('\n')

        # Run different winning scenarios
        if Thedealer.value > 21:
            dealer_busts(player_1_chips)

        elif Thedealer.value > player_1.value:
            dealer_wins(player_1_chips)

        elif Thedealer.value < player_1.value:
            player_wins(player_1_chips)

        else:
            push()   
    
    # Inform Player of their chips total 
    print(f'You bet {player_1_chips.bet}, you now have {player_1_chips.total} chips')
    print('-----------------End of round!-----------------')


    # Ask to play again
    x = input("Do you want to play another hand? Enter y or n\n").lower()
    if player_1_chips.total <= 0:
        print("\nYou ran outta chips :( Thank you for playing")
        break      
    elif x[0] == 'y' and player_1_chips.total > 0:
        print('-----------------Start of new round!-----------------')
        playing = True
        continue
    else:
        print("\nEnd of game! Thank you for playing")
        break
    
    
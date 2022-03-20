from card import Card
from player import Player
import itertools
import random


# Hardcoded game cards
suspects = ['Miss Scarlet', 'Col. Mustard', 'Mrs. White', 'Mr. Green', 'Mrs. Peacock', 'Prof. Plum']
weapons = ['Candlestick', 'Revolver', 'Dagger', 'Lead Pipe', 'Rope',' Wrench']
rooms = ['Study', 'Hall', 'Lounge', 'Library', 'Billiard Room', 'Dining Room', 'Conservatory', 'Ballroom', 'Kitchen']

# Hardcoded home square locations
home_locations = {'Miss Scarlet': 'H1',
                  'Col. Mustard': 'H2',
                  'Mrs. White': 'H3',
                  'Mr. Green': 'H4',
                  'Mrs. Peacock': 'H5',
                  'Prof. Plum': 'H6'}


class GameInitializer:
    def __init__(self, users):    
        self.suspect_cards = [Card('suspect',s) for s in suspects]
        self.weapon_cards = [Card('weapon',w) for w in weapons]
        self.room_cards = [Card('room',r) for r in rooms]
        self.game_cards = list(itertools.chain(self.suspect_cards, self.weapon_cards, self.room_cards))
        self.players = [Player(username = p[0], client_id = p[1]) for p in users.items()]
        self.n_players = len(self.players)

    def initialize_cards(self):
        '''Distribute cards to players, the case file envelope, and the extra cards'''
        random.shuffle(self.suspect_cards) # Shuffle suspect cards
        random.shuffle(self.weapon_cards) # Shuffle weapon cards
        random.shuffle(self.room_cards) # Shuffle room cards

        # Build the case file envelope
        self.case_file_cards = [self.suspect_cards[0], self.weapon_cards[0], self.room_cards[0]]
        self.suspect_cards[0].is_case_file_card = True
        self.weapon_cards[0].is_case_file_card = True
        self.room_cards[0].is_case_file_card = True

        # Assign each player a random card
        random.shuffle(self.game_cards) # Shuffle all the game cards

        # The number of cards each player gets is determined by the number of players in the game.
        if self.n_players == 3:
            draw_amount = 6
        if self.n_players == 4:
            draw_amount = 4
        if self.n_players == 5:
            draw_amount = 3
        if self.n_players == 6:
            draw_amount = 3

        for p in self.players:

            # Retrieve three unassigned cards
            unassigned_cards = list(filter(lambda card: card.is_case_file_card != True and\
                                    card.is_extra_card != True and\
                                    card.owner == None, self.game_cards))[0:draw_amount]
                                    
            for c in unassigned_cards:
                c.owner = p.username # Mark card owner
            p.cards = unassigned_cards

        self.extra_cards = list(filter(lambda card: card.is_case_file_card != True and\
                                card.is_extra_card != True and\
                                card.owner == None, self.game_cards))
        for ec in self.extra_cards:
            ec.is_extra_card = True # Mark extra card


    def assign_character_names(self):
        '''Each player in the game is assigned a character name'''
        counter = 0
        for p in self.players:
            p.character = self.suspect_cards[counter].name # Assign each player a random character
            counter += 1 


    def initialize_player_locations(self):
        '''Place players on their home squares'''
        for p in self.players:
            p.location = home_locations[p.character]
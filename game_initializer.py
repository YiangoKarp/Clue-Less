from asyncio.windows_events import NULL
from card import Card
from location import Location
import location
from player import Player
import itertools
import random


# Hardcoded game cards
suspects = ['Miss Scarlet', 'Col. Mustard', 'Mrs. White', 'Mr. Green', 'Mrs. Peacock', 'Prof. Plum']
weapons = ['Candlestick', 'Revolver', 'Dagger', 'Lead Pipe', 'Rope',' Wrench']
rooms = ['Study', 'Hall', 'Lounge', 'Library', 'Billiard Room', 'Dining Room', 'Conservatory', 'Ballroom', 'Kitchen']

# Hardcoded home square assignments
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

    def initialize_player_locations(self):
        '''Place players on their home squares'''
        for p in self.players:
            p.location = Location.locations[home_locations[p.character]] # Retrieve the Home Square Location object associated to the selected character.

    def generate_game_map(self):
        '''Generate a dictionary of the game map. The game map
        is provided in the course material.'''

        cols = ['A','B','C','D','E']
        rows = ['1', '2', '3', '4', '5']
        rooms = {'A1': 'Study', 'C1': 'Hall', 'E1': 'Lounge', 
                 'A3': 'Library', 'C3': 'Billiard Room', 
                 'E3': 'Dining Room', 'A5': 'Conservatory',
                 'C5': 'Ball Room', 'E5': 'Kitchen'}
        null_space = ['B2', 'D2', 'B4', 'D4'] # The map in the course material will show that those locations are null space.

        Location.locations = {} # Ensure that the locations variable is flushed before adding locations to it.

        # Declare the Location objects for all room and hallway squares.
        for c in cols:
            for r in rows:
                name = c+r # Name the square on the map using Alpha+Numeric (Ex: E1 is the Lounge Room)
                if name in null_space:
                    continue # That location on the Grid is not a square. It it just null space. Don't create a location.
                if name in rooms: # Lookup the square name to see if it is a room.
                    location_type = 'room' 
                else:
                    location_type = 'hallway'
                Location.locations[name] = Location(name, location_type)

        # Declare the location objects for the six home squares.
        for i in range(6):
            name = 'H'+str(i+1)
            location_type = 'home'
            Location.locations[name] = Location(name, location_type)

        # Hardcoded Adjacency Map
        adjacencies = {'A1': ['B1','A2','E5'],
                       'B1': ['A1','C1'],
                       'C1': ['B1','C2','D1'],
                       'D1': ['C1','E1'],
                       'E1': ['D1','E2','A5'],
                       'A2': ['A1', 'A3'],
                       'C2': ['C1','C3'],
                       'E2': ['E1','E3'],
                       'A3': ['A2','B3','A4'],
                       'B3': ['A3','C3'],
                       'C3': ['B3','C2','D3','C4'],
                       'D3': ['C3','E4'],
                       'E3': ['E1','D3','E4'],
                       'A4': ['A3','A5'],
                       'C4': ['C3','C5'],
                       'E4': ['E3','E5'],
                       'A5': ['A4','B5','E1'],
                       'B5': ['A5','C5'],
                       'C5': ['B5','C4','D5'],
                       'D5': ['C5','E5'],
                       'E5': ['D5','E4','A1'],
                       'H1': ['D1'],
                       'H2': ['E2'],
                       'H3': ['D5'],
                       'H4': ['B5'],
                       'H5': ['A4'],
                       'H6': ['A2']
                      }

        # Second pass of all the Location objects will assign the neighbors relative to each square.
        for key, value in Location.locations.items():
            neighbors = adjacencies[key] # Retrieve a list of adjacent squares for a square.
            for n in neighbors:
                loc_neighbor = Location.locations[n] # Get the Location object of the neighbor
                Location.locations[key].add_neighbors(loc_neighbor) # Add the neighbor to the Location object
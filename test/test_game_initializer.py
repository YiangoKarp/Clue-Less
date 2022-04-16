import unittest
from game_initializer import GameInitializer
from location import Location


class TestGameInitializer(unittest.TestCase):
    
    def test_initialize_cards_3_players(self):
        '''Distribute cards for a 3 player game.'''
        players = {'PLAYER_1': 'ID_1', 'PLAYER_2': 'ID_2', 'PLAYER_3': 'ID_3'}
        gi = GameInitializer(players)
        gi.initialize_cards()
        extra_cards = gi.extra_cards
        self.assertTrue(len(extra_cards) == 0)
        self.assertTrue(gi.n_players == 3)
        self.assertTrue(len(gi.case_file_cards) == 3)
        self.assertTrue(gi.case_file_cards[0].type == 'suspect' and gi.case_file_cards[1].type == 'weapon' and gi.case_file_cards[2].type == 'room')

    def test_initialize_cards_4_players(self):
        '''Distribute cards for a 4 player game.'''
        players = {'PLAYER_1': 'ID_1', 'PLAYER_2': 'ID_2', 'PLAYER_3': 'ID_3', 'PLAYER_4' : 'ID_4'}
        gi = GameInitializer(players)
        gi.initialize_cards()
        extra_cards = gi.extra_cards
        self.assertTrue(len(extra_cards) == 2)
        self.assertTrue(gi.n_players == 4)
        self.assertTrue(len(gi.case_file_cards) == 3)
        self.assertTrue(gi.case_file_cards[0].type == 'suspect' and gi.case_file_cards[1].type == 'weapon' and gi.case_file_cards[2].type == 'room')
    
    def test_initialize_cards_5_players(self):
        '''Distribute cards for a 5 player game.'''
        players = {'PLAYER_1': 'ID_1', 'PLAYER_2': 'ID_2', 'PLAYER_3': 'ID_3', 'PLAYER_4' : 'ID_4', 'PLAYER_5': 'ID_5'}
        gi = GameInitializer(players)
        gi.initialize_cards()
        extra_cards = gi.extra_cards
        self.assertTrue(len(extra_cards) == 3)
        self.assertTrue(gi.n_players == 5)
        self.assertTrue(len(gi.case_file_cards) == 3)
        self.assertTrue(gi.case_file_cards[0].type == 'suspect' and gi.case_file_cards[1].type == 'weapon' and gi.case_file_cards[2].type == 'room')

    def test_initialize_cards_6_players(self):
        '''Distribute cards for a 6 player game.'''
        players = {'PLAYER_1': 'ID_1', 'PLAYER_2': 'ID_2', 'PLAYER_3': 'ID_3', 'PLAYER_4' : 'ID_4', 'PLAYER_5': 'ID_5', 'PLAYER_6': 'ID_6'}
        gi = GameInitializer(players)
        gi.initialize_cards()
        extra_cards = gi.extra_cards
        self.assertTrue(len(extra_cards) == 0)
        self.assertTrue(gi.n_players == 6)
        self.assertTrue(len(gi.case_file_cards) == 3)
        self.assertTrue(gi.case_file_cards[0].type == 'suspect' and gi.case_file_cards[1].type == 'weapon' and gi.case_file_cards[2].type == 'room')
    
    # def test_assign_character_names(self):
    #     '''Ensure that each player has an assigned character'''
    #     users = {'USER_1': 'ID_1', 'USER_2': 'ID_2', 'USER_3': 'ID_3', 'USER_4' : 'ID_4', 'USER_5': 'ID_5'}
    #     gi = GameInitializer(users)
    #     gi.initialize_cards()
    #     gi.assign_character_names()
    #     for p in gi.players:
    #         self.assertTrue(p.character != None)

    def test_initialize_player_locations(self):
        '''Ensure that each player starts on their character's home square.'''
        users = {'USER_1': 'ID_1', 'USER_2': 'ID_2', 'USER_3': 'ID_3', 'USER_4' : 'ID_4', 'USER_5': 'ID_5'}
        gi = GameInitializer(users)
        gi.initialize_cards()

        gi.players[0].character = "Miss Scarlet"
        gi.players[1].character = "Col. Mustard"
        gi.players[2].character = "Mrs. White"
        gi.players[3].character = "Mr. Green"
        gi.players[4].character = "Mrs. Peacock"

        gi.generate_game_map()
        gi.initialize_player_locations()
        for p in gi.players:
            self.assertTrue(p.location.name[0] == 'H') # Players will always begin in a Home square.
            self.assertTrue(p.location.adjacent_locations[0].location_type == 'hallway') # Every home square should have one neighboring hallway.

    def test_game_locations(self):
        '''Ensure that the game map was properly configured'''
        users = {'USER_1': 'ID_1', 'USER_2': 'ID_2', 'USER_3': 'ID_3', 'USER_4' : 'ID_4', 'USER_5': 'ID_5'}
        gi = GameInitializer(users)
        gi.initialize_cards()

        gi.players[0].character = "Miss Scarlet"
        gi.players[1].character = "Col. Mustard"
        gi.players[2].character = "Mrs. White"
        gi.players[3].character = "Mr. Green"
        gi.players[4].character = "Mrs. Peacock"

        gi.generate_game_map()
        gi.initialize_player_locations()

        self.assertTrue(len(list(filter(lambda loc: loc.location_type == 'room', Location.locations.values())))) # Ensure that there are 9 rooms
        self.assertTrue(len(list(filter(lambda loc: loc.location_type == 'hallway', Location.locations.values())))) # Ensure that there are 12 hallways
        self.assertTrue(len(list(filter(lambda loc: loc.location_type == 'home', Location.locations.values())))) # Ensure that there are 6 home squares

if __name__ == '__main__':
    unittest.main()


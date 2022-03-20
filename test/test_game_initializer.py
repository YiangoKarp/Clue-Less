import unittest
from game_initializer import GameInitializer

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
        gi.assign_character_names()
        gi.initialize_player_locations()
        for p in gi.players:
            self.assertTrue(p.location[0] == 'H')

if __name__ == '__main__':
    unittest.main()


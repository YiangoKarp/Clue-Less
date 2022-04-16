import unittest
from game_initializer import GameInitializer
from game_manager import GameManager

class TestGameManager(unittest.TestCase):

    def test_game_manager_3_players(self):
        '''Distribute cards for a 3 player game.'''
        players = {'PLAYER_1': 'ID_1', 'PLAYER_2': 'ID_2', 'PLAYER_3': 'ID_3'}
        gi = GameInitializer(players)
        gi.initialize_cards()
        gm = GameManager(gi.players, gi.game_cards)
        self.assertFalse(gm.game_over)
        self.assertTrue(len(gm.cards) == 21)
        self.assertTrue(len(gm.players) == 3)
        self.assertTrue(gm.player_num_going == 0)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 1)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 2)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 0)
        player_going = gm.players[gm.player_num_going]
        end_turn = gm.run_turn(player_going)

    def test_game_manager_4_players(self):
        '''Distribute cards for a 4 player game.'''
        players = {'PLAYER_1': 'ID_1', 'PLAYER_2': 'ID_2', 'PLAYER_3': 'ID_3', 'PLAYER_4' : 'ID_4'}
        gi = GameInitializer(players)
        gi.initialize_cards()
        gm = GameManager(gi.players, gi.game_cards)
        self.assertFalse(gm.game_over)
        self.assertTrue(len(gm.cards) == 21)
        self.assertTrue(len(gm.players) == 4)
        self.assertTrue(gm.player_num_going == 0)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 1)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 2)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 3)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 0)
        player_going = gm.players[gm.player_num_going]
        #end_turn = gm.run_turn(player_going)

    def test_game_manager_5_players(self):
        '''Distribute cards for a 5 player game.'''
        players = {'PLAYER_1': 'ID_1', 'PLAYER_2': 'ID_2', 'PLAYER_3': 'ID_3', 'PLAYER_4' : 'ID_4', 'PLAYER_5': 'ID_5'}
        gi = GameInitializer(players)
        gi.initialize_cards()
        gm = GameManager(gi.players, gi.game_cards)
        self.assertFalse(gm.game_over)
        self.assertTrue(len(gm.cards) == 21)
        self.assertTrue(len(gm.players) == 5)
        self.assertTrue(gm.player_num_going == 0)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 1)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 2)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 3)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 4)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 0)
        player_going = gm.players[gm.player_num_going]
        #end_turn = gm.run_turn(player_going)

    def test_game_manager_6_players(self):
        '''Distribute cards for a 6 player game.'''
        players = {'PLAYER_1': 'ID_1', 'PLAYER_2': 'ID_2', 'PLAYER_3': 'ID_3', 'PLAYER_4' : 'ID_4', 'PLAYER_5': 'ID_5', 'PLAYER_6': 'ID_6'}
        gi = GameInitializer(players)
        gi.initialize_cards()
        gm = GameManager(gi.players, gi.game_cards)
        self.assertFalse(gm.game_over)
        self.assertTrue(len(gm.cards) == 21)
        self.assertTrue(len(gm.players) == 6)
        self.assertTrue(gm.player_num_going == 0)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 1)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 2)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 3)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 4)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 5)
        gm.move_to_next_turn()
        self.assertTrue(gm.player_num_going == 0)
        player_going = gm.players[gm.player_num_going]
        #end_turn = gm.run_turn(player_going)


if __name__ == '__main__':
    unittest.main()

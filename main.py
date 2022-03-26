#
# ░█████╗░██╗░░░░░██╗░░░██╗███████╗░░░░░░██╗░░░░░███████╗░██████╗░██████╗
# ██╔══██╗██║░░░░░██║░░░██║██╔════╝░░░░░░██║░░░░░██╔════╝██╔════╝██╔════╝
# ██║░░╚═╝██║░░░░░██║░░░██║█████╗░░█████╗██║░░░░░█████╗░░╚█████╗░╚█████╗░
# ██║░░██╗██║░░░░░██║░░░██║██╔══╝░░╚════╝██║░░░░░██╔══╝░░░╚═══██╗░╚═══██╗
# ╚█████╔╝███████╗╚██████╔╝███████╗░░░░░░███████╗███████╗██████╔╝██████╔╝
# ░╚════╝░╚══════╝░╚═════╝░╚══════╝░░░░░░╚══════╝╚══════╝╚═════╝░╚═════╝░

# EN.605.601.81.SP22 (Foundations of Software Engineering)
# Authors: Tenth Floor Cool Kids Club

# This game is a simplified version of the popular board game, Clue®. 
# The main simplification is in the navigation of the game board. 
# In Clue-Less there are the same nine rooms, six weapons, and six people as in the board game. 
# The rules are pretty much the same except for moving from room to room.

from http import server
import socket
import urllib.request
import time
import console_visuals
import sys
from tqdm import tqdm
from colorama import init
from colorama import Fore, Back, Style

from server_connection_handler import ServerConnectionHandler
from game_initializer import GameInitializer
from game_manager import GameManager

init() # Invoke console coloring


def main():
    
    sch = ServerConnectionHandler()
    sch.muster_clients()
    sch.broadcast('All players have joined. Starting game!')
    sch.broadcast(console_visuals.game_logo())

    available_characters = ['Miss Scarlet', 'Col. Mustard', 'Mrs. White', 'Mr. Green', 'Mrs. Peacock', 'Prof. Plum']

    gi = GameInitializer(sch.users) # Instantiate the GameInitializer module

    # Prompt each player to choose a character
    sch.broadcast('Users will now select their characters when it is their turn..')
    counter = 0
    for u in sch.users.items():
        selected_character = sch.choose_character(u[1], available_characters) # Get the players selected character
        sch.broadcast(f'User {u[0]} has selected character {selected_character}')
        gi.players[counter].character = selected_character # Assign this character to the player
        counter += 1
    
    gi.initialize_cards()
    gi.initialize_player_locations()

    # Randomize player turn order (add method to GameInitializer?)


    # Initialize Room objects (add method to GameInitializer?)


    # Assign adjacent_rooms to Room objects (add method to GameInitializer?)


    # Initialize GameManager
    gm = GameManager(gi.players, gi.game_cards)

    # Run the game
    while not gm.game_over:
        player_going = gm.players[gm.player_num_going]
        end_turn = gm.run_turn(player_going)
        if end_turn == "Accuse":
            end_accusation = gm.run_accusation(player_going)
        gm.move_to_next_turn()

    # End game using the information in the end_accusation object from gm.run_accusation
    # (basically just congratulate the winner properly, and then ask if they'd like to play again)


    # Need unit test for GameManager

    #users = {'USER_1': 'ID_1', 'USER_2': 'ID_2', 'USER_3': 'ID_3', 'USER_4' : 'ID_4', 'USER_5': 'ID_5'}
    # gi = GameInitializer(users)
    # gi.initialize_cards()
    # gi.initialize_player_locations()
    # print(gi.players[0])

if __name__ == '__main__':
    main()
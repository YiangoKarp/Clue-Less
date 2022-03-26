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

    #users = {'USER_1': 'ID_1', 'USER_2': 'ID_2', 'USER_3': 'ID_3', 'USER_4' : 'ID_4', 'USER_5': 'ID_5'}
    # gi = GameInitializer(users)
    # gi.initialize_cards()
    # gi.initialize_player_locations()
    # print(gi.players[0])

    # BRAINSTORMING
    # Steps of GameManager process
    # - GameManager receives as inputs: players, cards
    # - initialize Room objects (actually for GameInitializer?)
    # - randomize player order (actually for GameInitializer?)
    #   - GameManager will just use the order of the players input
    #   - inform players of order
    # - first turns for each player, in order
    #   - (everyone's first turn is moving from starting location to adjacent hallway)
    #   - broadcast player moves to everyone
    #   - update Player location
    #   - update Room players list
    # - typical turn for player1
    #   - GameManager sends player options (move options, suggest [if available], accuse)
    #       - move options determined by Room where player currently is
    #   - if player moves:
    #       - player chooses move option, choice sent back to GameManager
    #       - GameManager updates player's location
    #       - update room's players present
    #   - if no move options available:
    #       - message player
    #   -

    # CONSIDERATIONS
    # - how to denote that a player has already moved, already suggested, etc in a turn?

    # Methods needed
    # - (for many, receiving input from user - see assign_username in server_connection_handler for example)
    # - Use server_connection_handler's message_user and broadcast methods to message players
    # - SendOptions
    # - MovePlayer
    # - MakeSuggestion
    # - MakeAccusation
    #
    # - EndGame?

if __name__ == '__main__':
    main()
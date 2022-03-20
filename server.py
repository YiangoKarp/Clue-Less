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


from game_initializer import GameInitializer
init() # Invoke console coloring

clients = [] # Connection string of players that joined
users = {} # Usernames of players that joined

class ServerConnectionHandler():
    def __init__(self):
        self.n_players = 1#int(input('How many real players are there?: '))
        self.n_bots = 2#int(input('How many bots to add?: '))

        # self.server_type = int(input('''
        # How would you like to host the server?:
        # [1] Locally (LAN)
        # [2] Globally (WAN)
        # '''))
        self.server_type = 1

        total = self.n_players + self.n_bots
        if total > 6:
            print(Fore.RED + f'Error: The total number of players and bots is {total}. The maximum is 6!' + Style.RESET_ALL)
            sys.exit(1)
        if total < 3:
            print(Fore.RED + f'Error: The total number of players and bots is {total}. The minimum is 3!' + Style.RESET_ALL)
            sys.exit(1)


        # Select the IP to host from (Public or Private)
        if self.server_type == 1:
            host = '127.0.0.1'
        elif self.server_type == 2:
            try:
                host = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8') # Get public IP
            except Exception as network_error:
                print(Fore.RED + f'Error: Unable to resolve public IP address. Are you connected to the internet?' + Style.RESET_ALL)

        # Initialize Server
        print(f'Hosting server using IP: {host}')
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, 8080))
        self.server.listen(self.n_players)

    def broadcast(self,msg):
        '''Send a message to all clients'''
        for c in clients:
            c.send(f"{msg}".encode('utf-8'))
            print(f"{msg}".encode('utf-8'))

    def muster_clients(self):
        '''Server will accept incoming requests for clients to join until it reaches the number of players.'''
        pbar = tqdm(initial = 0, total = self.n_players, desc = 'Waiting for players to join.')
        while len(clients) < self.n_players:
            client, ip = self.server.accept()
            clients.append(client) # Add client to roster
            username = self.assign_username(client) # Prompt client for their username
            self.broadcast(Fore.BLUE + f'{username} has joined the game!' + Style.RESET_ALL)
            pbar.update(1)
        pbar.close()

    def assign_username(self,client):
        '''Request that the client provide a username'''
        client.send('What would you like your username to be?: '.encode('utf-8'))
        username = client.recv(3000).decode('utf-8')

        # TODO implement username validation and checking for duplicates

        users[username] = client # Save the username to client association
        client.send(f'Welcome, {username}!\n'.encode('utf-8'))
        return username


sch = ServerConnectionHandler()
sch.muster_clients()
sch.broadcast('All players have joined. Starting game!')
sch.broadcast(console_visuals.game_logo())


#users = {'USER_1': 'ID_1', 'USER_2': 'ID_2', 'USER_3': 'ID_3', 'USER_4' : 'ID_4', 'USER_5': 'ID_5'}
# gi = GameInitializer(users)
# gi.initialize_cards()
# gi.assign_character_names()
# gi.initialize_player_locations()
# print(gi.players[0])

# TODO Consider putting game flow in a main script
# TODO Create a logging class
# TODO Create a navigation table
# TODO Create a game initializer diagram
# TODO Create the Game Manager Class
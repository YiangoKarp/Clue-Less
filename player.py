# player.py

from checklist import Checklist

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from location import Location
    from card import Card
    from socket import socket

class Player:
    def __init__(self, username: str, client_id: 'socket', character: str = None, location: 'Location' = None, cards: 'Card' = None):
        self.username: str = username
        self.client_id: 'socket' = client_id
        self.character: str = character # A string of the name of the character
        self.location: 'Location' = location
        self.cards: 'Card' = cards
        #self.checklist = Checklist(cards)

        # Track if the player was moved by suggestion between turns -> will affect options on their turn
        # -> always reset at the end of player's turn
        self.was_suggested: bool = False
        self.eliminated: bool = False

    # def __repr__(self):
    #     '''Player print() function'''
    #     output = f'''
    #     Username: {self.username}
    #     Client ID: {self.client_id}
    #     Character: {self.character}
    #     Location: {self.location}
    #     Cards: {self.cards}
    #     Checklist: {self.checklist}
    #     '''
    #     return output

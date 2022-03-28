# turn.py
from player import Player
from location import Location
from card import Card


class Turn:
    def __init__(self, player):
        self.player = player
        self.moved = False
        self.suggested = False
        self.accused = False  # might be unnecessary

    def generate_player_options(self, player):
        options = []
        move_options = self.generate_player_move_options(player)

        # Player can only move if there are open locations next to their location and they have not already moved
        if len(move_options) > 0 and not self.moved:
            options.append("Move")

        # Player can suggest if they are in a room and they moved there or were moved there by a suggestion
        # and if they have not suggested yet
        if (self.moved or self.player.was_suggested) and player.location.location_type == "room" and not self.suggested:
            options.append("Suggest")

        # Player can accuse at any time during their turn
        options.append("Accuse")

        # Player can always end their turn
        options.append("End Turn")

        return options

    def generate_player_move_options(self, player):
        # Get locations adjacent to player's current location
        moves = player.location.adjacent_locations
        for move in moves:
            if not move.movable:
                moves.remove(move)
        return moves

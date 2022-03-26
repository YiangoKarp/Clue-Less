from card import Card
from player import Player
from location import Location
from turn import Turn


class GameManager:
    def __init__(self, players, cards):
        self.players = players
        self.cards = cards # Need to take cards as input because not all cards are held by players

    def run_turn(self, player):
        turn = Turn(player)
        player_options = turn.generate_player_options(player, turn)

        player_choice = turn.receive_player_choice(player, player_options)

        # While the player has not ended their turn or made an accusation:
        # 1. Execute player's choice,
        # 2. Generate player's options,
        # 3. Receive player's next choice
        while player_choice != "End Turn" and player_choice != "Accuse":
            # Execute player's choice
            if player_choice == "Move":
                player_move_options = turn.generate_player_move_options(player)
                # Receive player's move choice
                # Run move_player
            if player_choice == "Suggest":
                # Run make_suggestion

            player_options = turn.generate_player_options(player, turn)

            player_choice = turn.receive_player_choice(player, player_options)

        # Return player choice because it could end on End Turn or Accuse
        # GameManager will act differently, depending on the result of the turn
        return player_choice

    def receive_player_choice(self, player, player_options):
        options_prompt = "What would you like to do?: " + player_options[0]

        for option in player_options[1:]:
            options_prompt = options_prompt + option

        # Send options prompt to user and receive their choice as numeric input
        player.client_id.send(options_prompt.encode('utf-8'))
        player_choice = player.client_id.recv(3000).decode('utf-8')

        # Error handling for incorrect user input

        return player_choice

    def receive_player_move_choice(self, player, move_options):
        # Need to get to the point that this function returns the actual location object, not just the location name

        options_prompt = "Where would you like to move?: " + move_options.name[0]

        for option in move_options[1:]:
            options_prompt = options_prompt + option.name

        # Send options prompt to user and receive their choice as numeric input
        player.client_id.send(options_prompt.encode('utf-8'))
        player_choice = player.client_id.recv(3000).decode('utf-8')

        # Error handling for incorrect user input

        return player_choice

    #def move_player(self, player, location_a, location_b):


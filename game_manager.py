from card import Card
from player import Player
from location import Location
from turn import Turn


class GameManager:
    def __init__(self, players, cards):
        self.players = players
        self.cards = cards # Need to take cards as input because not all cards are held by players
        self.game_over = False
        self.player_num_going = 0 # To track where in the players list we are for turns

    def move_to_next_turn(self):
        if self.player_num_going + 1 == len(self.players):
            self.player_num_going = 0
        else:
            self.player_num_going = self.player_num_going + 1

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
                # Get the movement options available to the player
                player_move_options = turn.generate_player_move_options(player)
                # Receive player's move choice
                player_move_choice = self.receive_player_move_choice(player, player_move_options)
                # Move the player
                self.move_player(player, player_move_choice)
            if player_choice == "Suggest":
                # Get player's suggestion values for the character and weapon (room must be where the character is)
                suggestion_values = self.get_suggestion_values(player)
                suggested_character = suggestion_values[0]
                suggested_weapon = suggestion_values[1]

                # Don't need to pass the room as an argument since that's stored in the Player object
                self.make_suggestion(player, suggested_character, suggested_weapon)

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
        # move_options will be a list of Location objects (length at least 1, up to 4)

        options_prompt = "Where would you like to move?: " + move_options.name[0]

        for option in move_options[1:]:
            options_prompt = options_prompt + option.name

        # Send options prompt to user and receive their choice as numeric input
        player.client_id.send(options_prompt.encode('utf-8'))
        player_choice_name = player.client_id.recv(3000).decode('utf-8')

        # Error handling for incorrect user input

        # Find the Location object with the name selected by the player
        player_choice = move_options[0]
        i = 0
        while player_choice_name != player_choice.name:
            i = i + 1
            player_choice = move_options[i]

        return player_choice # Return the location object

    def move_player(self, player, new_location):
        # Update values of Location object for player's current location
        player.location.players_present.remove(player)
        if player.location.max_players > len(player.location.players_present):
            player.location.movable = True

        # Update player's location
        player.location = new_location

        # Update values of Location object for player's new location
        player.location.players_present.append(player)
        if player.location.max_players <= len(player.location.players_present):
            player.location.movable = False

    def get_suggestion_values(self, player):
        return

    def make_suggestion(self, player, suspect, weapon):
        return

    # Keep run_accusation separate from run_turn since run_turn either returns 'Accuse' or 'End Turn'
    # We will call run_turn and run_accusation separately in the main script
    def run_accusation(self, player):


        # If accusation is correct, set self.game_over to True
        # If len(self.players) < 2, set self.game_over to True
        return

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

        self.extra_cards = []
        self.case_file_cards = []
        for c in cards:
            if c.is_extra_card:
                self.extra_cards.append(c)
            if c.is_case_file_card:
                self.case_file_cards.append(c)

    def move_to_next_turn(self):
        if self.player_num_going + 1 == len(self.players):
            self.player_num_going = 0
        else:
            self.player_num_going = self.player_num_going + 1

    def run_turn(self, player):
        turn = Turn(player)
        player_options = turn.generate_player_options(player)

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
                # Get string names of character, weapon, and room for suggestion, in that order
                suggestion_values = self.get_suggestion_values(player)

                # Inform all players of the suggestion
                suggest_msg = player.username + " is making a suggestion: It was " + \
                              suggestion_values[0] + " in the " + suggestion_values[2] + "with the " + \
                              suggestion_values[1] + "!"
                self.broadcast(suggest_msg)

                # Find if any player is playing as the suggested character
                player_to_move = None
                for p in self.players:
                    if p.character == suggestion_values[0]:
                        player_to_move = p

                # If the player exists, move them
                if player_to_move is not None:
                    self.move_player(player_to_move, player.location)

                # Run the suggestion
                self.make_suggestion(player, suggestion_values)

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
        while player_choice not in player_options:
            error_options_prompt = "Invalid choice entered. " + options_prompt

            player.client_id.send(error_options_prompt.encode('utf-8'))
            player_choice = player.client_id.recv(3000).decode('utf-8')

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

        self.broadcast(player.username + " moved to " + new_location.name)

    # For the UI, we will have to change this to a pop-up or something
    def get_suggestion_values(self, player):
        suggest_char_prompt = """Which character committed the crime: 
        Miss Scarlet, Col. Mustard, Mrs. White, Mr. Green, Mrs. Peacock, or Prof. Plum?"""

        player.client_id.send(suggest_char_prompt.encode('utf-8'))
        suggest_char_choice = player.client_id.recv(3000).decode('utf-8')

        # Error handling for incorrect suggestion player input
        while suggest_char_choice not in self.character_name_list():
            suggest_char_prompt = """Invalid character name entered.
            Which character committed the crime: 
            Miss Scarlet, Col. Mustard, Mrs. White, Mr. Green, Mrs. Peacock, or Prof. Plum?"""

            player.client_id.send(suggest_char_prompt.encode('utf-8'))
            suggest_char_choice = player.client_id.recv(3000).decode('utf-8')

        suggest_weapon_prompt = """Which weapon was used for the crime: 
        candlestick, revolver, dagger, lead pipe, rope, or wrench?"""

        player.client_id.send(suggest_weapon_prompt.encode('utf-8'))
        suggest_weapon_choice = player.client_id.recv(3000).decode('utf-8')

        while suggest_weapon_choice not in self.weapon_name_list():
            suggest_weapon_prompt = """Invalid weapon name entered.
            Which weapon was used for the crime: 
            candlestick, revolver, dagger, lead pipe, rope, or wrench?"""

            player.client_id.send(suggest_weapon_prompt.encode('utf-8'))
            suggest_weapon_choice = player.client_id.recv(3000).decode('utf-8')

        # Return the names of the character, weapon, and room (3 strings)
        # Change to returning the cards? Or the names of the first 2 but then the Location object?
        suggestion_values = [suggest_char_choice, suggest_weapon_choice, player.location.name]

        return suggestion_values

    def make_suggestion(self, player, suggestion_values):
        # Get list of players from which to request a card
        players_to_request = self.players[:self.player_num_going] + self.players[self.player_num_going + 1:]

        request_ind = 0
        card_to_show = None

        while card_to_show is None & request_ind < len(players_to_request):
            showing_player = players_to_request[request_ind]
            showable_cards = []

            # Check if the player has a showable card
            for card in showing_player.cards:
                # suggestion_values is a list of card names
                if card.name in suggestion_values:
                    showable_cards.append(card.name)

            if len(showable_cards) == 0:
                # If 0 showable cards, message all players and move to next player
                suggest_msg = showing_player.username + " was unable to show a card!"
                self.broadcast(suggest_msg)
            else:
                # If 1 showable card, that's the card. Otherwise, prompt for card selection
                if len(showable_cards) == 1:
                    card_to_show = showable_cards[0]
                else:
                    # Create prompt for card to show
                    card_show_prompt = "Which card would you like to show? " + showable_cards[0]
                    for card_name in showable_cards[1:]:
                        card_show_prompt = card_show_prompt + " or " + card_name

                    showing_player.client_id.send(card_show_prompt.encode('utf-8'))
                    card_to_show = showing_player.client_id.recv(3000).decode('utf-8')

                    # Error handling if player enters incorrect value
                    while card_to_show not in showable_cards:
                        error_card_show_prompt = "That's not a showable card. " + card_show_prompt

                        showing_player.client_id.send(error_card_show_prompt.encode('utf-8'))
                        card_to_show = showing_player.client_id.recv(3000).decode('utf-8')

                # Finally, show the card to the suggesting player and tell all players a card was shown
                card_showing_prompt = showing_player.username + " shows you " + card_to_show

                player.client_id.send(card_showing_prompt.encode('utf-8'))

                self.broadcast(showing_player.username + " showed a card to " + player.username + "!")

                # Update player's checklist?
        return

    # Keep run_accusation separate from run_turn since run_turn either returns 'Accuse' or 'End Turn'
    # We will call run_turn and run_accusation separately in the main script
    def run_accusation(self, player):
        # Get accusation values
        accusation_values = self.get_accusation_values(player)

        # Broadcast to all players the accusation
        accuse_msg = player.username + " is making an ACCUSATION: It was " + \
                      accusation_values[0] + " in the " + accusation_values[2] + "with the " + \
                      accusation_values[1] + "!"
        self.broadcast(accuse_msg)

        # Check accusation values against answer
        correct_accuse = self.check_accusation_values(accusation_values)

        # If accusation is correct, set self.game_over to True
        if correct_accuse:
            self.broadcast(player.username + "'s accusation was correct!")
            self.game_over = True
        else: # If accusation is wrong, remove player from the players list



        # Need to be careful to adjust player_num_going if the player removed comes before the player going
        # in the players list

        # If len(self.players) < 2, set self.game_over to True

        return None

    # For the UI, we will have to change this to a pop-up or something
    def get_accusation_values(self, player):
        accuse_char_prompt = """Which character committed the crime: 
        Miss Scarlet, Col. Mustard, Mrs. White, Mr. Green, Mrs. Peacock, or Prof. Plum?"""

        player.client_id.send(accuse_char_prompt.encode('utf-8'))
        accuse_char_choice = player.client_id.recv(3000).decode('utf-8')

        # Error handling for incorrect suggestion player input
        while accuse_char_choice not in self.character_name_list():
            accuse_char_prompt = """Invalid character name entered.
            Which character committed the crime: 
            Miss Scarlet, Col. Mustard, Mrs. White, Mr. Green, Mrs. Peacock, or Prof. Plum?"""

            player.client_id.send(accuse_char_prompt.encode('utf-8'))
            accuse_char_choice = player.client_id.recv(3000).decode('utf-8')

        accuse_weapon_prompt = """Which weapon was used for the crime: 
        candlestick, revolver, dagger, lead pipe, rope, or wrench?"""

        player.client_id.send(accuse_weapon_prompt.encode('utf-8'))
        accuse_weapon_choice = player.client_id.recv(3000).decode('utf-8')

        while accuse_weapon_choice not in self.weapon_name_list():
            accuse_weapon_prompt = """Invalid weapon name entered.
            Which weapon was used for the crime: 
            candlestick, revolver, dagger, lead pipe, rope, or wrench?"""

            player.client_id.send(accuse_weapon_prompt.encode('utf-8'))
            accuse_weapon_choice = player.client_id.recv(3000).decode('utf-8')

        accuse_location_prompt = """Where did the crime happen: 
        Study, Hall, Lounge, Library, Billiard Room, Dining Room, Conservatory, Ballroom, or Kitchen?"""

        player.client_id.send(accuse_location_prompt.encode('utf-8'))
        accuse_location_choice = player.client_id.recv(3000).decode('utf-8')

        while accuse_location_choice not in self.location_name_list():
            accuse_location_prompt = """Invalid weapon name entered.
            Where did the crime happen: 
            Study, Hall, Lounge, Library, Billiard Room, Dining Room, Conservatory, Ballroom, or Kitchen?"""

            player.client_id.send(accuse_location_prompt.encode('utf-8'))
            accuse_location_choice = player.client_id.recv(3000).decode('utf-8')

        # Return the names of the character, weapon, and room (3 strings)
        # Change to returning the cards? Or the names of the first 2 but then the Location object?
        accusation_values = [accuse_char_choice, accuse_weapon_choice, accuse_location_choice]

        return accusation_values

    def check_accusation_values(self, accusation_values):
        correct_count = 0
        for acc_val in accusation_values:
            for c in self.case_file_cards:
                if acc_val == c.name:
                    correct_count = correct_count + 1

        if correct_count == 3:
            correct_accuse = True
        else:
            correct_accuse = False

        return correct_accuse

    def character_name_list(self):
        return ["Miss Scarlet", "Col. Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Prof. Plum"]

    def weapon_name_list(self):
        return ["candlestick", "revolver", "dagger", "lead pipe", "rope", "wrench"]

    def room_name_list(self):
        return ["Study", "Hall", "Lounge", "Library", "Billiard Room", "Dining Room", "Conservatory",
                "Ballroom", "Kitchen"]

    def broadcast(self, msg):
        '''Send a message to all clients'''
        print(f"[Broadcast Message] {msg}")
        for c in self.players:
            c.client.send(f"[Broadcast Message] {msg}\n".encode('utf-8'))

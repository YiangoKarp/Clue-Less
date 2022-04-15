# player.py

class Player:
    def __init__(self, username, client_id, character = None, location = None, cards = None, checklist = None):
        self.username = username
        self.client_id = client_id
        self.character = character # A string of the name of the character
        self.location = location
        self.cards = cards # A list of Card objects
        self.checklist = checklist
        # Track if the player was moved by suggestion between turns -> will affect options on their turn
        # -> always reset at the end of player's turn
        self.was_suggested = False

    def __repr__(self):
        '''Player print() function'''
        output = f'''
        Username: {self.username}
        Client ID: {self.client_id}
        Character: {self.character}
        Location: {self.location}
        Cards: {self.cards}
        Checklist: {self.checklist}
        '''
        return output
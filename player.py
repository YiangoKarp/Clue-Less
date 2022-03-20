# player.py

class Player:
    def __init__(self, username, client_id, character = None, location = None, cards = None, checklist = None):
        self.username = username
        self.client_id = client_id
        self.character = character
        self.location = location
        self.cards = cards
        self.checklist = checklist

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
# card.py

from queue import Empty

class Card:
    def __init__(self, type, name, is_case_file_card = False, is_extra_card = False, owner = None):
        self.type = type
        self.name = name
        self.is_case_file_card = is_case_file_card
        self.is_extra_card = is_extra_card
        self.owner = owner

    def __repr__(self):
        '''Card print() function'''
        output = f'''
        Card Type: {self.type}
        Card Name: {self.name}
        Case File Card?: {self.is_case_file_card}
        Card Owner: {self.owner}
        '''
        return output
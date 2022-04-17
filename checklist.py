from card import Card

suspects = ['Miss Scarlet', 'Col. Mustard', 'Mrs. White', 'Mr. Green', 'Mrs. Peacock', 'Prof. Plum']
weapons = ['Candlestick', 'Revolver', 'Dagger', 'Lead Pipe', 'Rope','Wrench']
rooms = ['Study', 'Hall', 'Lounge', 'Library', 'Billiard Room', 'Dining Room', 'Conservatory', 'Ballroom', 'Kitchen']

class Checklist():
    
    def __init__(self, starting_visible_cards):
        self.cards_in_game = suspects + weapons + rooms
        self.checked_off = [0 for c in self.cards_in_game] # array of 0 if unknown and 1 if known not to be guilty
        
        # check off the cards that the player either has or are visible to whole table
        for c in starting_visible_cards:
            i = 0
            for n in self.cards_in_game:
                if c.name == n:
                    self.checked_off[i] = 1
                    break
                i += 1
          
    def check_box(self, new_seen_card):
        i = 0
        for n in self.cards_in_game:
            if new_seen_card.name == n:
                self.checked_off[i] = 1
                break
            i += 1
    
    def __repr__(self):
        self.checklist_string = ""
        for i in range(len(self.cards_in_game)):
            if i == 0:
                self.checklist_string += '\nSuspects:\n----------\n'
            if i == 6:
                self.checklist_string += '\nWeapons:\n----------\n'
            if i == 12:
                self.checklist_string += '\nRooms:\n----------\n'
                
            if self.checked_off[i] == 1:
                self.checklist_string += '[x] '
            else:
                self.checklist_string += '[ ] '
                
            self.checklist_string += self.cards_in_game[i] + '\n'
            
        return self.checklist_string
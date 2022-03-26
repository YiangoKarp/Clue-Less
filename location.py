# location.py

class Location:
    def __init__(self, name, location_type, adjacent_locations = None, players_present = None):
        self.name = name
        self.location_type = location_type
        # Start adjacent_locations as None because we will need to initialize all locations before assigning neighbors
        self.adjacent_locations = adjacent_locations
        if self.location_type == "room":
            self.max_players = 6
        else:
            self.max_players = 1
        self.players_present = players_present
        self.movable = True

    def __repr__(self):
        '''Location print() function'''
        output = f'''
        Location Name: {self.name}
        Location Type: {self.location_type}
        Adjacent Locations: {self.adjacent_locations}
        Max Players: {self.max_players}
        Player Present: {self.players_present}
        Open to Move: {self.movable}
        '''
        return output

    def add_neighbors(self, neighbors):
        self.adjacent_locations = neighbors

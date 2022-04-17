# location.py

class Location:

    locations = {} # This static dictionary will hold all of the location objects on the game map.

    def __init__(self, name, location_type, players_present = [], room_name = None):
        self.name = name # Name of the square (Ex: A1)
        self.room_name = room_name # The name of the room (If it is a hallway, just call it 'hallway')
        self.location_type = location_type
        # Default adjacent_locations as empty because we will need to initialize all locations before assigning neighbors
        self.adjacent_locations = []
        if self.location_type == "room":
            self.max_players = 6
        else:
            self.max_players = 1
        self.players_present = players_present
        self.moveable = True

    def __repr__(self):
        '''Location print() function'''
        output = f'''
        Location Name: {self.name}
        Location Type: {self.location_type}
        Adjacent Locations: {self.adjacent_locations}
        Max Players: {self.max_players}
        Player Present: {self.players_present}
        Open to Move: {self.moveable}
        '''
        return output

    def add_neighbors(self, neighbors):
        self.adjacent_locations.append(neighbors)

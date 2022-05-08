# UI_Client.py

# EN.605.601.81.SP22 (Foundations of Software Engineering)
# Authors: Tenth Floor Cool Kids Club

from utils.Enums import EDirection

def Str2List(input: str):
    print("Str2List input: ", input)
    if input == "[]":
        return []
    else:
        return input.strip("][").replace("'", "").split(', ')

'''
def GetLocationID(location: str):
    if location == "H1":
        return "D1"
    elif location == "H2":
        return "E2"
    elif location == "H3":
        return "D5"
    elif location == "H4":
        return "B5"
    elif location == "H5":
        return "A4"
    elif location == "H6":
        return "A2"
    else:
        return location
'''

def GetMapCoord(location: str):
    '''
    Get Map Coord in Y,X format because I made the mistake
    '''
    if location == "A1":
        return (2, 2)
    elif location == "B1":
        return (5, 2)
    elif location == "C1":
        return (8, 2)
    elif location == "D1":
        return (11, 2)
    elif location == "E1":
        return (14, 2)
    elif location == "A2":
        return (2, 5)
    elif location == "C2":
        return (8, 5)
    elif location == "E2":
        return (14, 5)
    elif location == "A3":
        return (2, 8)
    elif location == "B3":
        return (5, 8)
    elif location == "C3":
        return (8, 8)
    elif location == "D3":
        return (11, 8)
    elif location == "E3":
        return (14, 8)
    elif location == "A4":
        return (2, 11)
    elif location == "C4":
        return (8, 11)
    elif location == "E4":
        return (14, 11)
    elif location == "A5":
        return (2, 15)
    elif location == "B5":
        return (5, 14)
    elif location == "C5":
        return (8, 14)
    elif location == "D5":
        return (11, 14)
    elif location == "E5":
        return (14, 14)
    elif location == "H1":
        return (11,1)
    elif location == "H2":
        return (15,5)
    elif location == "H3":
        return (11,15)
    elif location == "H4":
        return (5,15)
    elif location == "H5":
        return (1,11)
    elif location == "H6":
        return (1,5)
    else:
        return (-1, -1)

def GetMovableDirection(location: str):
    # print("GetMovableDirection with location: ", location)
    #from utils.Enums import EDirection
    if location == "A1":
        return [EDirection.Right, EDirection.Down, EDirection.TrapDoor]
    elif location == "B1":
        return [EDirection.Left, EDirection.Right]
    elif location == "C1":
        return [EDirection.Left, EDirection.Down, EDirection.Right]
    elif location == "D1":
        return [EDirection.Left, EDirection.Right]
    elif location == "E1":
        return [EDirection.Left, EDirection.Down, EDirection.TrapDoor]
    elif location == "A2":
        return [EDirection.Up, EDirection.Down]
    elif location == "C2":
        return [EDirection.Up, EDirection.Down]
    elif location == "E2":
        return [EDirection.Up, EDirection.Down]
    elif location == "A3":
        return [EDirection.Up, EDirection.Right, EDirection.Down]
    elif location == "B3":
        return [EDirection.Left, EDirection.Right]
    elif location == "C3":
        return [EDirection.Left, EDirection.Up, EDirection.Right, EDirection.Down]
    elif location == "D3":
        return [EDirection.Left, EDirection.Right]
    elif location == "E3":
        return [EDirection.Up, EDirection.Left, EDirection.Down]
    elif location == "A4":
        return [EDirection.Up, EDirection.Down]
    elif location == "C4":
        return [EDirection.Up, EDirection.Down]
    elif location == "E4":
        return [EDirection.Up, EDirection.Down]
    elif location == "A5":
        return [EDirection.Up, EDirection.Right, EDirection.TrapDoor]
    elif location == "B5":
        return [EDirection.Left, EDirection.Right]
    elif location == "C5":
        return [EDirection.Left, EDirection.Up, EDirection.Right]
    elif location == "D5":
        return [EDirection.Left, EDirection.Right]
    elif location == "E5":
        return [EDirection.Left, EDirection.Up, EDirection.TrapDoor]
    elif location == "H1":
        return [EDirection.Down]
    elif location == "H2":
        return [EDirection.Left]
    elif location == "H3":
        return [EDirection.Up]
    elif location == "H4":
        return [EDirection.Up]
    elif location == "H5":
        return [EDirection.Right]
    elif location == "H6":
        return [EDirection.Right]
    else:
        return []

def GetAdjacentLocation(location: str, moveTo: EDirection):
    """
    return a location id for sending to the server
    """
    adjacencies = {'A1': ['B1','A2','E5'],
                    'B1': ['A1','C1'],
                    'C1': ['B1','C2','D1'],
                    'D1': ['C1','E1'],
                    'E1': ['D1','E2','A5'],
                    'A2': ['A1', 'A3'],
                    'C2': ['C1','C3'],
                    'E2': ['E1','E3'],
                    'A3': ['A2','B3','A4'],
                    'B3': ['A3','C3'],
                    'C3': ['B3','C2','D3','C4'],
                    'D3': ['C3','E3'],
                    'E3': ['E2','D3','E4'],
                    'A4': ['A3','A5'],
                    'C4': ['C3','C5'],
                    'E4': ['E3','E5'],
                    'A5': ['A4','B5','E1'],
                    'B5': ['A5','C5'],
                    'C5': ['B5','C4','D5'],
                    'D5': ['C5','E5'],
                    'E5': ['D5','E4','A1'],
                    'H1': ['D1'],
                    'H2': ['E2'],
                    'H3': ['D5'],
                    'H4': ['B5'],
                    'H5': ['A4'],
                    'H6': ['A2']
                    }
    positionList = GetMovableDirection(location)
    index = positionList.index(moveTo)
    return adjacencies[location][index]

def GetAdjacentLocations(location: str):
    """
    return a list of adjacent locations
    """
    adjacencies = {'A1': ['B1','A2','E5'],
                    'B1': ['A1','C1'],
                    'C1': ['B1','C2','D1'],
                    'D1': ['C1','E1'],
                    'E1': ['D1','E2','A5'],
                    'A2': ['A1', 'A3'],
                    'C2': ['C1','C3'],
                    'E2': ['E1','E3'],
                    'A3': ['A2','B3','A4'],
                    'B3': ['A3','C3'],
                    'C3': ['B3','C2','D3','C4'],
                    'D3': ['C3','E3'],
                    'E3': ['E2','D3','E4'],
                    'A4': ['A3','A5'],
                    'C4': ['C3','C5'],
                    'E4': ['E3','E5'],
                    'A5': ['A4','B5','E1'],
                    'B5': ['A5','C5'],
                    'C5': ['B5','C4','D5'],
                    'D5': ['C5','E5'],
                    'E5': ['D5','E4','A1'],
                    'H1': ['D1'],
                    'H2': ['E2'],
                    'H3': ['D5'],
                    'H4': ['B5'],
                    'H5': ['A4'],
                    'H6': ['A2']
                    }
    return adjacencies[location]

def GetCharacterColor(character: str):
    if character == "Miss Scarlet": return "#FF0000" # red
    elif character == "Col. Mustard" : return "#FFFF00" # yellow
    elif character == "Mrs. White" : return "#00FFFF"   # cyan
    elif character == "Mr. Green" : return "#008000"    # green
    elif character == "Mrs. Peacock" : return "#0000FF" # blue
    elif character == "Prof. Plum" : return "#800080"   # purple
    else:
        return "#8B4513" # poo

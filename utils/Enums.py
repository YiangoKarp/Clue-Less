from enum import Enum

class EDirection(Enum):
    Up = "Up"
    Down = "Down"
    Left = "Left"
    Right = "Right"
    TrapDoor = "Trap Door"

# unused
class ELocation(Enum):
    Study = "A1",
    H1 = "B1",
    Hall = "C1",
    H2 = "D1",
    Lounge = "E1",
    H3 = "A2",
    H4 = "C2",
    H5 = "E2",
    Library = "A3",
    H6 = "B3",
    BillardRoom = "C3",
    H7 = "D3",
    DiningRoom = "E3",
    H8 = "A4",
    H9 = "C4",
    H10 = "E4",
    Conservatory = "A5",
    H11 = "B5",
    Ballroom = "C5",
    H12 = "D5",
    Kitchen = "E5"
'''
class ESuspect(Enum):
    MissScarlet = "Miss Scarlet"
    Col_Mustard = "Colonel Mustard"
    Mrs_White = "Mrs. White"
    Mr_Green = "Mr. Green"
    Mrs_Peacock = "Mrs. Peacock"
    Prof_Plum = "Prof. Plum"

class ESuspectColor(Enum):
    MissScarlet = "#FF0000" # red
    Col_Mustard = "#FFFF00" # yellow
    Mrs_White = "#00FFFF"   # cyan
    Mr_Green = "#008000"    # green
    Mrs_Peacock = "#0000FF" # blue
    Prof_Plum = "#800080"   # purple
'''
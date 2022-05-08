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

def GetCharacterColor(character: str):
    if character == "Miss Scarlet": return "#FF0000" # red
    elif character == "Col. Mustard" : return "#FFFF00" # yellow
    elif character == "Mrs. White" : return "#00FFFF"   # cyan
    elif character == "Mr. Green" : return "#008000"    # green
    elif character == "Mrs. Peacock" : return "#0000FF" # blue
    elif character == "Prof. Plum" : return "#800080"   # purple
    else:
        return "#8B4513" # poo

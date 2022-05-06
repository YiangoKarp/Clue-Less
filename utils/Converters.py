# UI_Client.py

# EN.605.601.81.SP22 (Foundations of Software Engineering)
# Authors: Tenth Floor Cool Kids Club

def Str2List(input: str):
    print("Str2List input: ", input)
    if input == "[]":
        return []
    else:
        return input.strip("][").replace("'", "").split(', ')
    
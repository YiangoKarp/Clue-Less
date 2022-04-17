from colorama import init
from colorama import Fore, Back, Style

def game_logo():
    game_logo = Fore.RED + '''
    ░█████╗░██╗░░░░░██╗░░░██╗███████╗░░░░░░██╗░░░░░███████╗░██████╗░██████╗
    ██╔══██╗██║░░░░░██║░░░██║██╔════╝░░░░░░██║░░░░░██╔════╝██╔════╝██╔════╝
    ██║░░╚═╝██║░░░░░██║░░░██║█████╗░░█████╗██║░░░░░█████╗░░╚█████╗░╚█████╗░
    ██║░░██╗██║░░░░░██║░░░██║██╔══╝░░╚════╝██║░░░░░██╔══╝░░░╚═══██╗░╚═══██╗
    ╚█████╔╝███████╗╚██████╔╝███████╗░░░░░░███████╗███████╗██████╔╝██████╔╝
    ░╚════╝░╚══════╝░╚═════╝░╚══════╝░░░░░░╚══════╝╚══════╝╚═════╝░╚═════╝░
    ''' + Style.RESET_ALL
    return(game_logo)

def suspects():
    '''Print the suspect options'''
    suspects = '''
    +----------------------+
    |      Suspects        |
    +----------------------+
    | [1] Miss Scarlet     |
    | [2] Col. Mustard     |
    | [3] Mrs. White       |
    | [4] Mr. Green        |
    | [5] Mrs. Peacock     |
    | [6] Prof. Plum       |
    +----------------------+
    '''
    return(suspects)

def weapons():
    '''Print the weapons options'''
    weapons = '''
    +----------------------+
    |       Weapons        |
    +----------------------+
    | [1] Candlestick      |
    | [2] Revolver         |
    | [3] Dagger           |
    | [4] Lead Pipe        |
    | [5] Rope             |
    | [6] Wrench           |
    +----------------------+
    '''
    return(weapons)

def options():
    '''Print the options for suspect and weapon'''
    options = '''
    +----------------------+-----------------+
    |      Suspects        |     Weapons     |
    +----------------------+-----------------+
    | [1] Miss Scarlet     | [1] Candlestick |
    | [2] Col. Mustard     | [2] Revolver    |
    | [3] Mrs. White       | [3] Dagger      |
    | [4] Mr. Green        | [4] Lead Pipe   |
    | [5] Mrs. Peacock     | [5] Rope        |
    | [6] Prof. Plum       | [6] Wrench      |
    +----------------------+-----------------+
    '''
    return(options)

def rooms():
    '''Print all the room options'''
    rooms = '''
    +-------------------+
    |      Rooms        |
    +-------------------+
    | [1] Study         |
    | [2] Hall          |
    | [3] Lounge        |
    | [4] Library       |
    | [5] Billiard Room |
    | [6] Dining Room   |
    | [7] Conservatory  |
    | [8] Ballroom      |
    | [9] Kitchen       |
    +-------------------+
    '''
    return(rooms)

def player_suggestion(murderer, weapon, room):
    suggestion = Fore.YELLOW + f'''
    +----------------------+
           SUGGESTION     
    +----------------------+
    * Murderer: {murderer} 
    * Weapon: {weapon}     
    * Room: {room}         
    +----------------------+
    ''' + Style.RESET_ALL
    return(suggestion)

def player_accusation(murderer, weapon, room):
    accusation = Fore.RED + f'''
    +----------------------+
           ACCUSATION      
    +----------------------+
    * Murderer: {murderer} 
    * Weapon: {weapon}     
    * Room: {room}         
    +----------------------+
    ''' + Style.RESET_ALL

def game_map():
    '''Print the game map'''
    map = f'''
            A       B        C       D         E
         _______          _______          _________
        |       |________|       |___H1___|         |
    1   | Study  ________  Hall   ________  Lounge  |
        |__   __|        |__   __|        |__    ___|
           | |              | |              |  |
    2    H6| |              | |              |  |H2
         __| |__          __| |__          __|  |___
        |       |________|       |________|         |
    3   |Library _________Billiard________  Dining  |
        |__   __|        |__   __|        |__    ___|
           | |              | |              |  |
    4    H5| |              | |              |  |
         __| |__          __| |__          __|  |___
        |       |________|       |________|         |
    5   |Conserv ________Ball Room_________ Kitchen |
        |_______|   H4   |_______|   H3   |_________|
    '''
    return(map)

def extra_cards(extra_cards):
    '''Print the extra cards on the board'''
    cards_names = [ card.name for card in extra_cards]
    cards_string = ', '.join(cards_names)
    extra_cards = f'Extra Cards: {cards_names}'
    return extra_cards

def player_cards(player):
    '''Print the cards a specific player has'''
    cards_names = [ card.name for card in player.cards]
    cards_string = ', '.join(cards_names)
    player_cards = f'Your Cards: {cards_names}'
    return player_cards

def case_file_envelope(end_accusation):
    '''Print the contents of the case file envelope'''
    case_file = f'''
    Here are the contents of the case file:   
    +----------------------+
       Case File Envelope    
    +----------------------+
    * Murderer: {end_accusation['murderer']} 
    * Weapon: {end_accusation['weapon']}     
    * Room: {end_accusation['room']}         
    +----------------------+
    '''
    return case_file


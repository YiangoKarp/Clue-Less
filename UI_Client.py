# UI_Client.py

# EN.605.601.81.SP22 (Foundations of Software Engineering)
# Authors: Tenth Floor Cool Kids Club
# darkmode color design guide: https://uxdesign.cc/dark-mode-ui-design-the-definitive-guide-part-1-color-53dcfaea5129
# style sheet: https://doc.qt.io/qt-5/stylesheet-reference.html

from operator import ne
import sys
import threading
from functools import partial

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QTextCursor

from client import Client

from utils import Converters, Append, Enums

#region reference
SUSPECTS = ['Miss Scarlet', 'Col. Mustard', 'Mrs. White', 'Mr. Green', 'Mrs. Peacock', 'Prof. Plum']
WEAPONS = ['Candlestick', 'Revolver', 'Dagger', 'Lead Pipe', 'Rope','Wrench']
ROOMS = ['Study', 'Hall', 'Lounge', 'Library', 'Billiard Room', 'Dining Room', 'Conservatory', 'Ballroom', 'Kitchen']
#endregion reference
#region global variables
_IsGameSessionJoined = False
_ServerAddress = ""
_PlayerName = ""
_PlayerCharacter = ""
_PlayerCards = []
_PlayerOptionsTemp = []
_LivingCharacters = []
_PlayerLocation = ""
_PlayerLocations = {}
#endregion global variables

class MainWindow(QMainWindow):

    #region binding pyqtSignal
    s_connect = pyqtSignal(bool)
    s_playerName = pyqtSignal()
    s_startGame = pyqtSignal()
    s_assignCharacter = pyqtSignal(list)
    s_serverBroadCast = pyqtSignal(str)
    s_assignCards = pyqtSignal(list)
    s_actionOptions = pyqtSignal(list)
    s_locationUpdate = pyqtSignal(dict)
    s_availableLocations = pyqtSignal(list)
    s_showCards = pyqtSignal(list)
    s_addClue = pyqtSignal(str)
    s_eliminated = pyqtSignal()
    s_gameOver = pyqtSignal(str)
    #endregion binding pyqtSignal

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(".\\views\\ClueStart_Main.ui", self)
        self.intializeComponents()
        self.signalBinding()
        self.show()

    def intializeComponents(self):
        #region GUI styling
        self.ui.Widget_ConfirmPlayer.setVisible(False)
        self.ui.Widget_GamePlay.setVisible(False)
        self.ui.Widget_GamePlay_Actions.setVisible(False)
        self.ui.Widget_GamePlay_PickCharacter.setVisible(False)
        self.ui.Widget_GamePlay_ShowCards.setVisible(False)
        self.ui.Widget_GamePlay_Waiting.setVisible(False)
        #endregion GUI styling
        #region GUI action binding
        self.ui.Btn_JoinServer.clicked.connect(self.joinServer)
        self.ui.Btn_ConfirmPlayer.clicked.connect(self.sendPlayerName)
        #endregion GUI action binding

    def signalBinding(self):
        self.s_connect.connect(self.updateJoinServerGUI)
        self.s_playerName.connect(self.enterPlayerName)
        self.s_startGame.connect(self.startGame)
        self.s_assignCharacter.connect(self.pickCharacter)
        self.s_serverBroadCast.connect(self.showBroadCast)
        self.s_assignCards.connect(self.assignCards)
        self.s_actionOptions.connect(self.setActionOptions)
        self.s_locationUpdate.connect(self.updateMap)
        self.s_availableLocations.connect(self.getAvailableMovement)
        self.s_showCards.connect(self.showCardsView)
        self.s_addClue.connect(self.showClues)
        self.s_eliminated.connect(self.eliminated)
        self.s_gameOver.connect(self.gameOver)

    def closeEvent(self, e):
        global _IsGameSessionJoined
        if _IsGameSessionJoined:
            answer = QMessageBox.question(
                window, None,
                "A game session is connected. Close the game?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if answer == QMessageBox.StandardButton.Yes:
                app.quit()
            else:
                e.ignore()
        else:
            app.quit()

#region join game
    def joinServer(self):
        serverAddress = self.ui.Entry.text()
        if len(serverAddress) == 0 or not serverAddress or serverAddress.isspace():
            print("No server address")
        else:
            # strip before connecting
            serverAddress = serverAddress.strip()
            global _ServerAddress
            _ServerAddress = serverAddress
            self.createGameClient()
            
    def createGameClient(self):
        global _ServerAddress
        self.clientThread = QThread()
        self.gameClient = Client(self, _ServerAddress)
        self.gameClient.moveToThread(self.clientThread)
        self.clientThread.start()

    def updateJoinServerGUI(self, isConnected: bool):
        if isConnected:
            self.ui.Btn_JoinServer.setText("Enjoy!")
            self.ui.Btn_JoinServer.setEnabled(False)
            # remove any error messages
            self.ui.Label_JoinErrorMsg.setText("")
            global _IsGameSessionJoined
            _IsGameSessionJoined = True
        else:
            global _ServerAddress
            self.ui.Label_JoinErrorMsg.setText(f"Unable to connect to host {_ServerAddress}. Is the server currently running?")
            self.ui.Btn_JoinServer.setText("Join Server")
            self.ui.Btn_JoinServer.setEnabled(True)
            _ServerAddress = ""
        pass

    def enterPlayerName(self):
        print("enterPlayerName")
        self.ui.Widget_JoinServer.setVisible(False)
        self.ui.Widget_ConfirmPlayer.setVisible(True)
    
    def sendPlayerName(self):
        global _PlayerName
        _PlayerName = self.ui.Entry_2.text()
        self.gameClient.tx_server(_PlayerName)
        self.ui.Widget_GamePlay_Waiting.setVisible(True)
#endregion join game

#region Game play functions
    def startGame(self):
        self.ui.Widget_GameInit.setVisible(False)
        # set grid minimum size
        for i in range(15):
            self.ui.GamePlay_MapGrid.setRowMinimumHeight(i, 20)
            self.ui.GamePlay_MapGrid.setColumnMinimumWidth(i, 20)
        self.ui.Widget_GamePlay.setVisible(True)
        self.ui.Widget_GamePlay_Waiting.setVisible(True)
        self.ui.GamePlay_ServerBM.setText("Game is ready")
        self.bindGamePlayEvents()
        self.disableAllActions()

    def bindGamePlayEvents(self):
        self.ui.GamePlay_Action_Suggest.clicked.connect(partial(self.sendActionChoice, "Suggest"))
        self.ui.GamePlay_Action_Accuse.clicked.connect(partial(self.sendActionChoice, "Accuse"))
        self.ui.GamePlay_Action_EndTurn.clicked.connect(partial(self.sendActionChoice, "End Turn"))
        self.ui.GamePlay_Action_Move.clicked.connect(partial(self.sendActionChoice, "Move"))

        self.ui.GamePlay_NavRight.clicked.connect(partial(self.sendMovement, Enums.EDirection.Right))
        self.ui.GamePlay_NavLeft.clicked.connect(partial(self.sendMovement, Enums.EDirection.Left))
        self.ui.GamePlay_NavUp.clicked.connect(partial(self.sendMovement, Enums.EDirection.Up))
        self.ui.GamePlay_NavDown.clicked.connect(partial(self.sendMovement, Enums.EDirection.Down))
        self.ui.GamePlay_NavTrapDoor.clicked.connect(partial(self.sendMovement, Enums.EDirection.TrapDoor))

    def pickCharacter(self, characterOptions: list):
        self.ui.PickCharacter_comboBox.addItems(characterOptions)
        self.ui.PickCharacter_comboBox.setCurrentIndex(0)
        self.ui.Widget_GamePlay_Waiting.setVisible(False)
        self.ui.Widget_GamePlay_PickCharacter.setVisible(True)
        self.ui.PickCharacter_ConfirmBtn.clicked.connect(self.confirmPickedCharacter)
        print("options: ", characterOptions)
    
    def confirmPickedCharacter(self):
        selection = self.ui.PickCharacter_comboBox.currentIndex() + 1
        # save and set GUI: GamePlay_PlayerCharacter
        global _PlayerCharacter
        _PlayerCharacter = self.ui.PickCharacter_comboBox.itemData(self.ui.PickCharacter_comboBox.currentIndex(), 2) # QUserRole=2, voodoo magic. don't know what that is.
        self.ui.GamePlay_PlayerCharacter.setText(_PlayerCharacter)
        color = Converters.GetCharacterColor(_PlayerCharacter)
        self.ui.GamePlay_PlayerCharacter.setStyleSheet(f"color: {color};")
        self.gameClient.tx_server(str(selection))
        self.ui.Widget_GamePlay_PickCharacter.setVisible(False)

    def assignCards(self, listOfCards: list):
        self.ui.GamePlay_PlayerCards.addItems(listOfCards)
        global _PlayerCards
        _PlayerCards = listOfCards

    def setActionOptions(self, options: list):
        global _PlayerOptionsTemp
        _PlayerOptionsTemp = options
        for i in options:
            if i == "Move":
                self.ui.GamePlay_Action_Move.setEnabled(True)
                self.ui.GamePlay_Action_Move.setFlat(False)
            if i == "Suggest":
                self.ui.GamePlay_Action_Suggest.setEnabled(True)
                self.ui.GamePlay_Action_Suggest.setFlat(False)
        # accuse and endturn always available
        self.ui.GamePlay_Action_Accuse.setEnabled(True)
        self.ui.GamePlay_Action_Accuse.setFlat(False)
        self.ui.GamePlay_Action_EndTurn.setEnabled(True)
        self.ui.GamePlay_Action_EndTurn.setFlat(False)
        
    def sendActionChoice(self, option: str):
        try:
            global _PlayerOptionsTemp
            index = _PlayerOptionsTemp.index(option)
            if option == "Suggest":
                self.showActionDetailView(option)
            elif option == "Accuse":
                self.showActionDetailView(option)
            elif option == "Move":
                # self.getAvailableMovement()
                # disable other options explicitly
                self.disableOtherActions()
            elif option == "End Turn":
                self.disableAllActions()
            self.gameClient.tx_server(str(index+1))
        except ValueError as vError:
            print(f"This shouldn't happen {vError}")
        except Exception as error:
            print(f"WTF {error}")
    
    def showActionDetailView(self, option: str):
        self.ui.Actions_ConfirmBtn.setText(option)
        # assign option styling
        if option == "Suggest":
            self.ui.Actions_ConfirmBtn.setStyleSheet("background: #626262; color: #FFFFFF")
        elif option == "Accuse":
            self.ui.Actions_ConfirmBtn.setText(option)
            self.ui.Actions_ConfirmBtn.setStyleSheet("background: #cf2c2b; color: #FFFFFF")
        else:
            self.ui.Actions_ConfirmBtn.setText(f"This is not correct: {option}")
        global _LivingCharacters
        self.ui.Actions_SuspectComboBox.addItems(_LivingCharacters)
        self.ui.Actions_WeaponComboBox.addItems(WEAPONS.copy())
        self.ui.Actions_RoomComboBox.addItems(ROOMS.copy())
        self.ui.Actions_SuspectComboBox.setCurrentIndex(0)
        self.ui.Actions_WeaponComboBox.setCurrentIndex(0)
        self.ui.Actions_RoomComboBox.setCurrentIndex(0)
        # bind buttons event
        self.ui.Actions_ConfirmBtn.clicked.connect(partial(self.runAction, False))
        self.ui.Actions_CancelBtn.clicked.connect(partial(self.runAction, True))
        # show view
        self.ui.Widget_GamePlay_Actions.setVisible(True)
    
    def runAction(self, isCanceled: False):
        # get values
        suspect = self.ui.Actions_SuspectComboBox.itemData(self.ui.Actions_SuspectComboBox.currentIndex(), 2)
        room = self.ui.Actions_RoomComboBox.itemData(self.ui.Actions_RoomComboBox.currentIndex(), 2)
        weapon = self.ui.Actions_WeaponComboBox.itemData(self.ui.Actions_WeaponComboBox.currentIndex(), 2)
        # suggestion values order: suspect, room, weapon.
        if not isCanceled:
            result = f"{suspect}@{room}@{weapon}"
            self.gameClient.tx_server(result)
        self.ui.Widget_GamePlay_Actions.setVisible(False)

    def getAvailableMovement(self, options: list):
        print("getAvailableMovement")
        global _PlayerLocation
        fullDirection = Converters.GetMovableDirection(_PlayerLocation)
        adjacentLocations = Converters.GetAdjacentLocations(_PlayerLocation)
        availableIndexes = []
        for availableLocation in options:
            try:
                index = adjacentLocations.index(availableLocation)
                availableIndexes.append(index)
            except ValueError as error:
                pass
        availableDirection = [fullDirection[i] for i in availableIndexes]
        for j in availableDirection:
            if j == Enums.EDirection.Right:
                self.ui.GamePlay_NavRight.setEnabled(True)
                self.ui.GamePlay_NavRight.setFlat(False)
            elif j == Enums.EDirection.Left:
                self.ui.GamePlay_NavLeft.setEnabled(True)
                self.ui.GamePlay_NavLeft.setFlat(False)
            elif j == Enums.EDirection.Up:
                self.ui.GamePlay_NavUp.setEnabled(True)
                self.ui.GamePlay_NavUp.setFlat(False)
            elif j == Enums.EDirection.Down:
                self.ui.GamePlay_NavDown.setEnabled(True)
                self.ui.GamePlay_NavDown.setFlat(False)    
            elif j == Enums.EDirection.TrapDoor:
                self.ui.GamePlay_NavTrapDoor.setEnabled(True)
                self.ui.GamePlay_NavTrapDoor.setFlat(False)
                
    def sendMovement(self, moveTo: Enums.EDirection):
        global _PlayerLocation, _PlayerLocations, _PlayerCharacter
        nextLocation = Converters.GetAdjacentLocation(_PlayerLocation, moveTo)
        print("NextLocation: ", nextLocation)
        self.gameClient.tx_server(nextLocation)
        self.disableAllMovement()
        # modify local map
        _PlayerLocations[_PlayerCharacter] = nextLocation
        self.updateMap(_PlayerLocations)

    def updateMap(self, locations: dict):
        '''
        Update the game map items on the grid
        dictionary format: {characterName, location}
        '''
        '''
        QGridLayout available positional function(s):
        addItem(item,row=,column=)
        removeItem(item) this doesn't have positional data

        All items size should be 21x21, larger than that will cause significant misalignment on the map.
        The row and column index also starts from 1 instead of 0, because 0 is used for styling in qt designer.
        '''
        '''
        Map coordinates reference:
        xx 1  2  3  4  5  6  7  8  9  10 11 12 13 14 15
        1  A1 A1 A1          C1 C1 C1    H1    E1 E1 E1
        2  A1 A1 A1 B1 B1 B1 C1 C1 C1 D1 D1 D1 E1 E1 E1
        3  A1 A1 A1          C1 C1 C1          E1 E1 E1
        4     A2                C2                E2
        5  H6 A2                C2                E2 H2
        6     A2                C2                E2
        7  A3 A3 A3          C3 C3 C3          E3 E3 E3
        8  A3 A3 A3 B3 B3 B3 C3 C3 C3 D3 D3 D3 E3 E3 E3
        9  A3 A3 A3          C3 C3 C3          E3 E3 E3
        10    A4                C4                E4
        11 H5 A4                C4                E4
        12    A4                C4                E4
        13 A5 A5 A5          C5 C5 C5          E5 E5 E5
        14 A5 A5 A5 B5 B5 B5 C5 C5 C5 D5 D5 D5 E5 E5 E5
        15 A5 A5 A5    H4    C5 C5 C5    H3    E5 E5 E5

        Center point of each area (Y,X):
        Study(A1): (2,2)
        Hall(C1): (8,2)
        Lounge(E1): (14,2)
        Library(A3): (2,8)
        Billard(C3): (8,8)
        Dining(E3): (14,8)
        Conserv(A5): (2,14)
        Ball Room(C5): (8,14)
        Kitchen(E5): (14,14)

        if trap door  (Y,X):
            Study(A1): (3,3)
            Lounge(E1): (13,3)
            Conserv(A5): (3,13)
            Kitchen(E5): (13,13)
        '''
        print(f"Locations Update Map: {locations}")
        global _PlayerLocations
        # hard clear
        for i in reversed(range(self.ui.GamePlay_MapGrid.count())): 
            widget = self.ui.GamePlay_MapGrid.itemAt(i).widget()
            if "background: #00000000;" not in widget.styleSheet():
                widget.deleteLater()

        isLocationSet = False
        for character, location in locations.items():
            # get character color
            characterColor = Converters.GetCharacterColor(character)
            # characterLocationID = Converters.GetLocationID(location)
            characterLocationID = location
            global _PlayerCharacter
            if not isLocationSet:
                if character == _PlayerCharacter:
                    global _PlayerLocation
                    _PlayerLocation = characterLocationID
                    isLocationSet = True
            characterMapCoord = Converters.GetMapCoord(characterLocationID)
            print(f"{character} Map Coord: {characterMapCoord[1]}, {characterMapCoord[0]}")
            point = QFrame()
            point.setStyleSheet(f"font-family: 'Segoe UI'; font-size: 12pt; background: {characterColor};")
            point.setFixedHeight(20)
            point.setFixedWidth(20)
            self.ui.GamePlay_MapGrid.addWidget(point,characterMapCoord[1],characterMapCoord[0])
        _PlayerLocations = locations
        # also update the living characters
        global _LivingCharacters
        tList = list(locations.keys())
        self.populatePlayerList(tList)
        tList.remove(_PlayerCharacter)
        _LivingCharacters = tList 

    def populatePlayerList(self, players: list):
        # generate HTML code
        html = ""
        for player in players:
            color = Converters.GetCharacterColor(player)
            html += f"<span style=\"color:{color};font-size: 16pt; font-family: \"Segoe UI\";\">{player}<br></span>\n"
        self.ui.GamePlay_PlayerList.setHtml(html)

    def showCardsView(self, options: list):
        self.ui.Widget_GamePlay_ShowCards.setVisible(True)
        self.ui.ShowCards_ComboBox.addItems(options)
        self.ui.ShowCards_ComboBox.setCurrentIndex(0)
        # bind button event
        self.ui.ShowCards_ConfirmBtn.clicked.connect(self.showCardToPlayer)

    def showCardToPlayer(self):
        card = self.ui.ShowCards_ComboBox.itemData(self.ui.ShowCards_ComboBox.currentIndex(), 2)
        self.gameClient.tx_server(card)
        self.ui.Widget_GamePlay_ShowCards.setVisible(False)

    def showBroadCast(self, msg: str):
        existingMsg = self.ui.GamePlay_ServerBM.toPlainText()
        self.ui.GamePlay_ServerBM.setText(Append.AddMessage(existingMsg, msg))
        self.ui.GamePlay_ServerBM.moveCursor(QTextCursor.MoveOperation.End)

    def showClues(self, msg: str):
        existingMsg = self.ui.GamePlay_ObtainedClues.toPlainText()
        self.ui.GamePlay_ObtainedClues.setText(Append.AddMessage(existingMsg, msg))
        self.ui.GamePlay_ObtainedClues.moveCursor(QTextCursor.MoveOperation.End)
    
    def eliminated(self):
        print("END")
    
    def gameOver(self, player: str):
        print(f"{player} is the killer. Game Over")
#endregion Game play functions  

    def disableAllActions(self):
        '''
        Disable all action buttons before players turn and after
        '''
        self.ui.GamePlay_NavDown.setEnabled(False)
        self.ui.GamePlay_NavDown.setFlat(True)
        self.ui.GamePlay_NavLeft.setEnabled(False)
        self.ui.GamePlay_NavLeft.setFlat(True)
        self.ui.GamePlay_NavRight.setEnabled(False)
        self.ui.GamePlay_NavRight.setFlat(True)
        self.ui.GamePlay_NavTrapDoor.setEnabled(False)
        self.ui.GamePlay_NavTrapDoor.setFlat(True)
        self.ui.GamePlay_NavUp.setEnabled(False)
        self.ui.GamePlay_NavUp.setFlat(True)
        self.ui.GamePlay_Action_Move.setEnabled(False)
        self.ui.GamePlay_Action_Move.setFlat(True)
        self.ui.GamePlay_Action_Suggest.setEnabled(False)
        self.ui.GamePlay_Action_Suggest.setFlat(True)
        self.ui.GamePlay_Action_Accuse.setEnabled(False)
        self.ui.GamePlay_Action_Accuse.setFlat(True)
        self.ui.GamePlay_Action_EndTurn.setEnabled(False)
        self.ui.GamePlay_Action_EndTurn.setFlat(True)

    def disableAllMovement(self):
        self.ui.GamePlay_NavDown.setEnabled(False)
        self.ui.GamePlay_NavDown.setFlat(True)
        self.ui.GamePlay_NavLeft.setEnabled(False)
        self.ui.GamePlay_NavLeft.setFlat(True)
        self.ui.GamePlay_NavRight.setEnabled(False)
        self.ui.GamePlay_NavRight.setFlat(True)
        self.ui.GamePlay_NavTrapDoor.setEnabled(False)
        self.ui.GamePlay_NavTrapDoor.setFlat(True)
        self.ui.GamePlay_NavUp.setEnabled(False)
        self.ui.GamePlay_NavUp.setFlat(True)
        self.ui.GamePlay_Action_Move.setEnabled(False)
        self.ui.GamePlay_Action_Move.setFlat(True)

    def disableOtherActions(self):
        self.ui.GamePlay_Action_Suggest.setEnabled(False)
        self.ui.GamePlay_Action_Suggest.setFlat(True)
        self.ui.GamePlay_Action_Accuse.setEnabled(False)
        self.ui.GamePlay_Action_Accuse.setFlat(True)
        self.ui.GamePlay_Action_EndTurn.setEnabled(False)
        self.ui.GamePlay_Action_EndTurn.setFlat(True)

app = QApplication(sys.argv)
window = MainWindow()
app.exec()

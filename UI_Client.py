# UI_Client.py

# EN.605.601.81.SP22 (Foundations of Software Engineering)
# Authors: Tenth Floor Cool Kids Club
# darkmode color design guide: https://uxdesign.cc/dark-mode-ui-design-the-definitive-guide-part-1-color-53dcfaea5129
# style sheet: https://doc.qt.io/qt-5/stylesheet-reference.html

import sys
import threading
from functools import partial

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from client import Client

from utils import Converters, Append

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
    s_moveOptions = pyqtSignal(list)
    s_locationUpdate = pyqtSignal(dict)
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
        self.s_moveOptions.connect(self.showMoveOptions)
        self.s_locationUpdate.connect(self.updateMap)
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
        pass
    
    def sendPlayerName(self):
        global _PlayerName
        _PlayerName = self.ui.Entry_2.text()
        self.gameClient.tx_server(_PlayerName)
        self.ui.Widget_GamePlay_Waiting.setVisible(True)
#endregion join game

#region Game play functions
    def startGame(self):
        self.ui.Widget_GameInit.setVisible(False)
        self.ui.Widget_GamePlay.setVisible(True)
        self.ui.Widget_GamePlay_Waiting.setVisible(True)
        self.ui.GamePlay_ServerBM.setText("Game is ready")
        self.bindGamePlayEvents()

    def bindGamePlayEvents(self):
        self.ui.GamePlay_Action_Suggest.clicked.connect(partial(self.sendActionChoice, "Suggest"))
        self.ui.GamePlay_Action_Accuse.clicked.connect(partial(self.sendActionChoice, "Accuse"))
        self.ui.GamePlay_Action_EndTurn.clicked.connect(partial(self.sendActionChoice, "End Turn"))

    def pickCharacter(self, characterOptions: list):
        self.ui.PickCharacter_comboBox.addItems(characterOptions)
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
        self.gameClient.tx_server(str(selection))
        self.ui.Widget_GamePlay_PickCharacter.setVisible(False)
        # save other characters to a separate list
        global _LivingCharacters
        tempList = SUSPECTS.copy()
        tempList.remove(_PlayerCharacter)
        _LivingCharacters = tempList

    def assignCards(self, listOfCards: list):
        self.ui.GamePlay_PlayerCards.addItems(listOfCards)
        global _PlayerCards
        _PlayerCards = listOfCards

    def setActionOptions(self, options: list):
        global _PlayerOptionsTemp
        _PlayerOptionsTemp = options
        # disable all buttons, and set text color to gray
        self.ui.GamePlay_NavDown.setEnabled(False)
        self.ui.GamePlay_NavLeft.setEnabled(False)
        self.ui.GamePlay_NavRight.setEnabled(False)
        self.ui.GamePlay_NavTrapDoor.setEnabled(False)
        self.ui.GamePlay_NavUp.setEnabled(False)
        self.ui.GamePlay_Action_Suggest.setEnabled(False)
        #self.ui.GamePlay_Action_Accuse.setEnabled(False)
        #self.ui.GamePlay_Action_EndTurn.setEnabled(False)
        self.ui.GamePlay_NavDown.setFlat(True)
        self.ui.GamePlay_NavLeft.setFlat(True)
        self.ui.GamePlay_NavRight.setFlat(True)
        self.ui.GamePlay_NavTrapDoor.setFlat(True)
        self.ui.GamePlay_NavUp.setFlat(True)
        self.ui.GamePlay_Action_Suggest.setFlat(True)
        #self.ui.GamePlay_Action_Accuse.setFlat(True)
        #self.ui.GamePlay_Action_EndTurn.setFlat(True)
        for i in options:
            if i == "Move":
                # this should based on the map location, enable all for now
                self.ui.GamePlay_NavDown.setEnabled(True)
                self.ui.GamePlay_NavLeft.setEnabled(True)
                self.ui.GamePlay_NavRight.setEnabled(True)
                self.ui.GamePlay_NavTrapDoor.setEnabled(True)
                self.ui.GamePlay_NavUp.setEnabled(True)
                self.ui.GamePlay_NavDown.setFlat(False)
                self.ui.GamePlay_NavLeft.setFlat(False)
                self.ui.GamePlay_NavRight.setFlat(False)
                self.ui.GamePlay_NavTrapDoor.setFlat(False)
                self.ui.GamePlay_NavUp.setFlat(False)
            if i == "Suggest":
                self.ui.GamePlay_Action_Suggest.setEnabled(True)
                self.ui.GamePlay_Action_Suggest.setFlat(False)
            '''
            always true
            if i == "Accuse":
                self.ui.GamePlay_Action_Accuse.setEnabled(True)
                self.ui.GamePlay_Action_Accuse.setFlat(False)
            if i == "End Turn":
                self.ui.GamePlay_Action_EndTurn.setEnabled(True)
                self.ui.GamePlay_Action_EndTurn.setFlat(False)
            '''

    def sendActionChoice(self, option: str):
        try:
            global _PlayerOptionsTemp
            index = _PlayerOptionsTemp.index(option)
            self.gameClient.tx_server(str(index+1))
            if option != "End Turn":
                self.showActionDetailView(option)
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
        else:
            self.ui.Widget_GamePlay_Actions.setVisible(False)
    
    def showMoveOptions(self, locations: list):
        #dynamic binding?
        print(f"movable locations: {locations}")

    def updateMap(self, locations: dict):
        '''
        Update the game map items on the grid
        '''
        '''
        QGridLayout available positional function(s):
        addItem(item,row=,column=)
        removeItem(item) this doesn't have positional data

        All items size should be 21x21, larger than that will cause significant misalignment on the map.
        The row and column index also starts from 1 instead of 0, because 0 is used for styling in qt designer.
        '''
        print(f"Locations: {locations}")
        

    def showCardsView(self, options: list):
        self.ui.Widget_GamePlay_ShowCards.setVisible(True)
        self.ui.ShowCards_ComboBox.addItems(options)
        # bind button event
        self.ui.ShowCards_ComfirmBtn.clicked.connect(self.showCardToPlayer)

    def showCardToPlayer(self):
        card = self.ui.ShowCards_ComboBox.itemData(self.ui.ShowCards_ComboBox.currentIndex(), 2)
        self.gameClient.tx_server(card)

    def showBroadCast(self, msg: str):
        existingMsg = self.ui.GamePlay_ServerBM.toPlainText()
        self.ui.GamePlay_ServerBM.setText(Append.AddMessage(existingMsg, msg))

    def showClues(self, msg: str):
        existingMsg = self.ui.GamePlay_ObtainedClues.toPlainText()
        self.ui.GamePlay_ObtainedClues.setText(Append.AddMessage(existingMsg, msg))

    def eliminated(self):
        print("END")
    
    def gameOver(self, player: str):
        print(f"{player} is the killer. Game Over")

#endregion Game play functions  
        

app = QApplication(sys.argv)
window = MainWindow()
app.exec()

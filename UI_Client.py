# UI_Client.py

# EN.605.601.81.SP22 (Foundations of Software Engineering)
# Authors: Tenth Floor Cool Kids Club
# darkmode color design guide: https://uxdesign.cc/dark-mode-ui-design-the-definitive-guide-part-1-color-53dcfaea5129
# style sheet: https://doc.qt.io/qt-5/stylesheet-reference.html

import sys
import threading

from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from client import Client

from utils import Converters, Append

#region global variables
_IsGameSessionJoined = False
_ServerAddress = ""
_PlayerName = ""
_PlayerCharacter = ""
_PlayerCards = []
#endregion global variables

class MainWindow(QMainWindow):

    #region binding pyqtSignal
    s_connect = pyqtSignal(bool)
    s_playerName = pyqtSignal()
    s_startGame = pyqtSignal()
    s_assignCharacter = pyqtSignal(list)
    s_serverBroadCast = pyqtSignal(str)
    s_assignCards = pyqtSignal(list)
    s_moveOptions = pyqtSignal(list)
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
        self.s_moveOptions.connect(self.setMoveOptions)

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
        # change button to enter game
        self.ui.Btn_JoinServer.setText("Enter")
        self.ui.Btn_JoinServer.setEnabled(True)
        # spawn enter nane ui
        self.ui.EntryLabel.setText("PlayerName")
        self.ui.Entry.setText("")
        pass
    
    def sendPlayerName(self):
        global _PlayerName
        _PlayerName = self.ui.Entry_2.text()
        self.gameClient.tx_server(_PlayerName)
        self.ui.Widget_GamePlay_Waiting.setVisible(True)

    def startGame(self):
        self.ui.Widget_GameInit.setVisible(False)
        self.ui.Widget_GamePlay.setVisible(True)
        self.ui.Widget_GamePlay_Waiting.setVisible(True)
        self.ui.GamePlay_ServerBM.setText("Game is ready")

    def pickCharacter(self, characterOptions: list):
        self.ui.PickCharacter_comboBox.addItems(characterOptions)
        self.ui.Widget_GamePlay_Waiting.setVisible(False)
        self.ui.Widget_GamePlay_PickCharacter.setVisible(True)
        self.ui.PickCharacter_ConfirmBtn.clicked.connect(self.confirmPickedCharacter)
        print("options: ", characterOptions)
    
    def confirmPickedCharacter(self, isCanceled: bool):
        if isCanceled:
            self.ui.Widget_GamePlay_PickCharacter.setVisible(False)
        else:
            selection = self.ui.PickCharacter_comboBox.currentIndex() + 1
            # save and set GUI: GamePlay_PlayerCharacter
            global _PlayerCharacter
            _PlayerCharacter = self.ui.PickCharacter_comboBox.itemData(self.ui.PickCharacter_comboBox.currentIndex(), 2) # QUserRole=2, voodoo magic. don't know what that is.
            self.ui.GamePlay_PlayerCharacter.setText(_PlayerCharacter)
            self.gameClient.tx_server(str(selection))
            self.ui.Widget_GamePlay_PickCharacter.setVisible(False)

    def assignCards(self, listOfCards: list):
        self.ui.GamePlay_PlayerCards.addItems(listOfCards)

    def setMoveOptions(self, options: list):
        # disable all buttons, and set text color to gray
        self.ui.GamePlay_NavDown.setEnabled(False)
        self.ui.GamePlay_NavLeft.setEnabled(False)
        self.ui.GamePlay_NavRight.setEnabled(False)
        self.ui.GamePlay_NavTrapDoor.setEnabled(False)
        self.ui.GamePlay_NavUp.setEnabled(False)
        self.ui.GamePlay_Action_Suggest.setEnabled(False)
        self.ui.GamePlay_Action_Accuse.setEnabled(False)
        self.ui.GamePlay_Action_EndTurn.setEnabled(False)
        self.ui.GamePlay_NavDown.setFlat(True)
        self.ui.GamePlay_NavLeft.setFlat(True)
        self.ui.GamePlay_NavRight.setFlat(True)
        self.ui.GamePlay_NavTrapDoor.setFlat(True)
        self.ui.GamePlay_NavUp.setFlat(True)
        self.ui.GamePlay_Action_Suggest.setFlat(True)
        self.ui.GamePlay_Action_Accuse.setFlat(True)
        self.ui.GamePlay_Action_EndTurn.setFlat(True)
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
            if i == "Accuse":
                self.ui.GamePlay_Action_Accuse.setEnabled(True)
                self.ui.GamePlay_Action_Accuse.setFlat(False)
            if i == "End Turn":
                self.ui.GamePlay_Action_EndTurn.setEnabled(True)
                self.ui.GamePlay_Action_EndTurn.setFlat(False)

    def showBroadCast(self, msg: str):
        existingMsg = self.ui.GamePlay_ServerBM.text()
        self.ui.GamePlay_ServerBM.setText(Append.AddMessage(existingMsg, msg))
    
        

app = QApplication(sys.argv)
window = MainWindow()
app.exec()

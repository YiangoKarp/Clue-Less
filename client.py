# client.py

# EN.605.601.81.SP22 (Foundations of Software Engineering)
# Authors: Tenth Floor Cool Kids Club

import sys
import threading
import socket

from PyQt6.QtCore import QThread, pyqtSignal, QObject

from utils import Converters

class Client(QThread):
    s_connect = pyqtSignal(bool)
    s_playerName = pyqtSignal()
    s_startGame = pyqtSignal()
    s_assignCharacter = pyqtSignal(list)
    s_serverBroadCast = pyqtSignal(str)
    s_assignCards = pyqtSignal(list)
    s_moveOptions = pyqtSignal(list)

    def __init__(self, parent, serverAddress: str):
        super().__init__()
        self.host = serverAddress
        self.gui = parent
        self.connectSocket()
        self.signalBinding()

    def signalBinding(self):
        self.s_connect.connect(self.gui.s_connect.emit)
        self.s_playerName.connect(self.gui.s_playerName.emit)
        self.s_startGame.connect(self.gui.s_startGame.emit)
        self.s_assignCharacter.connect(self.gui.s_assignCharacter.emit)
        self.s_serverBroadCast.connect(self.gui.s_serverBroadCast.emit)
        self.s_assignCards.connect(self.gui.s_assignCards.emit)
        self.s_moveOptions.connect(self.gui.s_moveOptions.emit)

    def connectSocket(self):
        try:
            print('Attempting Connection..')
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, 8080))
            print('Connection Successful!')
        except Exception as connection_failed:
            print(f'Error: Unable to connect to host {self.host}. Is the server currently running?')
            self.s_connect.emit(False)

        rx_thread = threading.Thread(target=self.rx_server, daemon = True) # Receive communication on a separate thread
        rx_thread.start()
        self.s_connect.emit(True)

    def tx_server(self, input: str):
        '''Transmit communication to server'''
        try:
            self.client.send(input.encode('utf-8'))
        except Exception as tx_error:
            print(f'Error: Unable to message server: {tx_error}')
            

    def rx_server(self):
        '''Receive communication from server.'''
        '''
        Changed binding message:
        1. AssignUserName: What would you like your username to be?: 
        2. BM_GameReady: [Broadcast Message] All players have joined.
        3. AssignCharacter@[options]: Please choose a character: \n{options}
        '''
        while 1:
            try:
                msg = self.client.recv(3000).decode('utf-8')
                if msg:
                    if(msg == 'kick'):
                        print('You have been disconnected from the server.')
                        self.client.shutdown(socket.SHUT_RDWR)
                        self.client.close()
                    else:
                        if msg == "AssignUserName":
                            print("self.s_playerName.emit()")
                            self.s_playerName.emit()
                        elif msg == "BM_GameReady":
                            self.s_startGame.emit()
                        elif "AssignCharacter@" in msg:
                            msg = msg.split("@")[1]
                            characterOptions = Converters.Str2List(msg)
                            self.s_assignCharacter.emit(characterOptions)
                        elif "PlayerCard@" in msg:
                            msg = msg.split("@")[1]
                            cards = Converters.Str2List(msg)
                            self.s_assignCards.emit(cards)
                            print(f"PlayerCards: {cards}\n")
                        elif "ExtraCard@" in msg:
                            msg = msg.split("@")[1]
                            cards = Converters.Str2List(msg)
                            print(f"ExtraCards: {cards}\n")
                            self.s_assignCards.emit(cards)
                        elif "PlayerMoveOption@" in msg:
                            msg = msg.split("@")[1]
                            options = Converters.Str2List(msg)
                            print(f"MoveOptions: {options}\n")
                            self.s_moveOptions.emit(options)
                        elif "BM_" in msg:
                            # pipe every BM_ to server broad cast board
                            self.s_serverBroadCast.emit(msg.replace("BM_",""))
                        else:
                            print("Unrecognized message: ", msg)
                else:
                    print("no message?")
                    break
            except Exception as rx_error:
                print(rx_error)
                self.s_connect.emit(False)
                break
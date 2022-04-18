# client.py

# EN.605.601.81.SP22 (Foundations of Software Engineering)
# Authors: Tenth Floor Cool Kids Club

import threading
import socket

from colorama import init
from colorama import Fore, Back, Style
init() # Invoke console coloring


class Client:
    def __init__(self):
        self.host = '127.0.0.1'#input("Please enter the host's IP: ")

        try:
            print('Attempting Connection..')
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, 8080))
            print('Connection Successful!')
        except Exception as connection_failed:
            print(f'Error: Unable to connect to host {self.host}. Is the server currently running?')
        
    def tx_server(self):
        '''Transmit communication to server'''
        while 1:
            try:
                self.client.send(input().encode('utf-8'))
            except Exception as tx_error:
                print(f'Error: Unable to message server: {tx_error}')
                break

    def rx_server(self):
        '''Receive communication from server.'''
        while 1:
            try:
                msg = self.client.recv(3000).decode('utf-8')
                if msg:
                    if(msg == 'kick'):
                        #print('You have been disconnected from the server.')
                        self.client.shutdown(socket.SHUT_RDWR)
                        self.client.close()
                    else:
                        print(msg)
                else:
                    break
            except Exception as rx_error:
                print('You have been disconnected from the server.')
                break


c = Client() # Receive communication on a separate thread
rx_thread = threading.Thread(target=c.rx_server, daemon = True) # Receive communication on a separate thread
rx_thread.start()
c.tx_server() # Transmit communication from the main thread

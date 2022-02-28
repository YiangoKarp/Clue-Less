# client.py

# EN.605.601.81.SP22 (Foundations of Software Engineering)
# Authors: Tenth Floor Cool Kids Club

import threading
import socket

from colorama import init
from colorama import Fore, Back, Style
init() # Invoke console coloring


host = input("Please enter the host's IP: ")

try:
    print('Attempting Connection..')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, 8080))
    print('Connection Successful!')
except Exception as connection_failed:
    print(f'Error: Unable to connect to host {host}. Is the server currently running?')

def tx_server():
    '''Transmit communication to server'''
    while 1:
        try:
            client.send(input().encode('utf-8'))
        except Exception as tx_error:
            print(f'Error: Unable to message server: {tx_error}')
            break

def rx_server():
    '''Receive communication from server.'''
    while 1:
        try:
            msg = client.recv(3000).decode('utf-8')
            if msg:
                print(msg)
            else:
                break
        except Exception as rx_error:
            print(f'Error: Unable to receive from server: {rx_error}')
            break


rx_thread = threading.Thread(target=rx_server, daemon = True) # Receive communication on a separate thread
rx_thread.start()
tx_server() # Transmit communication from the main thread

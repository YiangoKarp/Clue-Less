# This an example of how we can simulate game scenarios. We can programatically run through user I/O.

import time
import socket


def print_response(client):
    print(client.recv(3000).decode('utf-8'))
    time.sleep(0.25)

def create_client(host = '127.0.0.1'):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((host,8080))
    time.sleep(0.25)
    return c

def client_login(client,username):
    client.send(str(username).encode('utf-8'))
    time.sleep(0.25)
    print_response(client)

def select_character(client, character_choice):
    client.send(str(character_choice).encode('utf-8'))
    time.sleep(0.25)
    print_response(client)


def stub_1():
    '''Simulates a game scenario'''

    # Open three client applications
    c1 = create_client()
    c2 = create_client()
    c3 = create_client()

    # Each user chooses a username
    client_login(c1, 'Player1')
    client_login(c2, 'Player2')
    client_login(c3, 'Player3')

    # Each user selects a character
    select_character(c1, '1')
    select_character(c2, '2')
    select_character(c3, '2')

    print_response(c1)

    time.sleep(1000000) # Prevents client connections from closing

if __name__ == '__main__':
    stub_1()


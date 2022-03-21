# Clue-Less

This repo will host efforts to build the Clue-Less game.


## Code Walkthrough

Refer to the *diagrams* folder to see the breakdown of the different components.

### main.py
This script is the driver of the game server. It will be responsible for controlling all sub-systems:
* Server Connection Handler
* Game Initializer
* Game Manager
* **Additional sub-systems?**

### server_connection_handler.py
This class manages the server-client functions. This includes connecting to the server, messaging users, and prompting for user input.

### game_initializer.py
This class is used to setup a game before it begins. It is responsible for drawing cards to players and the case file envelope, allowing users to choose their characters, and assigning each character to their home square location.

### client.py
This script is used by players to connect to the server. It uses two threads; one for transmitting messages to the server and the other one for receiving messages from the server.

### GUI Implementation
The target framework for the GUI implementation is *PyQt*. The development for a GUI will begin once we have created the console version of the game. 
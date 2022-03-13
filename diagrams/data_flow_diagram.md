```mermaid

graph TD

RP[Requesting Player] --> | Connection Request | 0((0. Game Lobby))
0 --> | Add Player | PR[Player Roster]
PR --> 0
SC[Server Configuration] --> 0
PR --> | Initialize Game | 1.1((1.1 Deal Cards))
1.1 --> CF[Case File Cards]
1.1 --> 1.2((1.2 Assign Player Cards))
1.2 --> PC[Player Cards]
1.2 --> EC[Extra Cards]
1.2 --> 1.3((1.3 Display Extra Cards in GUI))
1.2 --> 2((2 Spawn Players))
2 --> PL[Player Locations]
PL --> 1.4((Update Player Locations in GUI)) 
2 --> | Initial Turn |3.1((3.1 Toggle Player Turn))
3.1 --> TT[Turn Tracker]
TT --> 3.1

3.1 --> | Player Suggestion | 3.3((3.3 Validate Player Room))
PL --> 3.3
3.3 --> | Invalid Suggestion | 3.1
3.3 --> | Valid Suggestion | 3.2((3.2 Teleport Suggested Player))
3.2 --> | Update Player Location | PL
3.2 --> ST[Suggestions Table]
3.2 --> 3.7((3.7 ??))
3.2 --> | Player to the left | PR
PR --> | Check if player has any of the cards | PC
PC --> | Left Player has any of the suggested three cards | 4.1((4.1 Choose card to share))
4.1 --> PCC[Player Card Checklist]
PCC --> TT

PC --> | Left Player has none of the suggested cards | 4.2((4.2 Get next Left Player))
4.2 --> PR
PR --> | Check if player has any of the cards | PC
4.2 --> 4.3((4.3 No players have suggested cards))
4.3 --> | Accuse Player | 3.4((3.4 Validate Accusation))
4.3 --> TT


3.1 --> | Accuse Player | 3.4
CF --> 3.4
3.4 --> | Correct Accusation | 3.5((3.5 END GAME))
3.4 --> | Incorrect Accusation | 3.6((3.6 Eliminate Player))
3.4 --> AT[Accusations Table]
3.6 --> PR
PR --> | One active player remaining | 3.5
3.6 --> PL
3.6 --> 3.1
3.6 --> TT

3.1 --> | Player Navigation | NL[Navigation Lookup Table]
NL --> | Valid Navigation | PL
NL --> | Invalid Navigation | 3.1
PL --> 3.1


```
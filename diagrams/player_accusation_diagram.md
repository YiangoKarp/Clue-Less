```mermaid

graph TD

A((Accusation)) --> CF[Check Case File]
CF --> | Correct Accusation | E[End Game]
E --> GM((Game Manager))
CF --> | Incorrect Accusation | EP[Eliminate Player]
EP --> GM
```
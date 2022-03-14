```mermaid

graph TD

PT((Player's Turn)) --> S[Suggestion]
PT --> A[Accusation]
PT --> N[Navigation]
S --> FT((Finish Turn))
A --> FT
N --> FT
FT --> | Next Player | PT
```
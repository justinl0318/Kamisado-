# Kamisado

### Intro to Kamisado
Kamisado is an abstract strategy board game for two players that's played on an 8x8 multicoloured board. Each player controls a set of eight octagonal dragon tower pieces. Each player's set of dragon towers contains a tower to match each of the colours that appear on the squares of the board (i.e., a brown tower, a green tower, etc.). [https://en.wikipedia.org/wiki/Kamisado](url)

### Intro to negamax algorithm
The _negamax_ algorithm is an algorithm frequently used in two-player games where it can search and analyze all futures moves (according to depth). It is a variant of the _minimax_ algorithm, where it relies on the fact `min(a, b) = -max(-b, -a)`.

### Description  
This project was written in _Python_ and _PyGame_. One of the player is controlled by the user, and the other is controlled by the AI Computer.  
The AI computer was developed with the negamax algorithm, along with _alpha_beta_pruning_ to shorten the depth of the search tree. 

The player can select the AI computer as the opponent in the home screen, and chooses the maximum `depth` of the search tree (i.e. the maximum number of future moves the AI can search for) in the home screen.      

The deeper the tree, the longer it takes for the AI to make a move.

#### Time estimate
| Depth | 3      | 4      | 5      |
| ----- | ------ | ------ | ------ |
| ---   | ~10 sec| ~1 min | ~3 min |

---

Youtube tutorial: [https://www.youtube.com/watch?v=adqrJB_LE6k](url)

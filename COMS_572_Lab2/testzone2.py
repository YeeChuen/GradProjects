# Author: Yee Chuen Teoh
# Title: testzone2


from checkersgame import checkers


gamestate = checkers()
gamestate.printboard(gamestate.initial)

moves = gamestate.actions(gamestate.initial)
print(moves)
gamestate.result(gamestate.initial, moves[2])
gamestate.printboard(gamestate.initial)

moves = gamestate.actions(gamestate.initial)
print(moves)
gamestate.result(gamestate.initial, moves[2])
gamestate.printboard(gamestate.initial)

moves = gamestate.actions(gamestate.initial)
print(moves)
gamestate.result(gamestate.initial, moves[2])
gamestate.printboard(gamestate.initial)

moves = gamestate.actions(gamestate.initial)
print(moves)
gamestate.result(gamestate.initial, moves[0])
gamestate.printboard(gamestate.initial)

# input
input1 = input()
  
# output
print(input1)
# Author: Yee Chuen Teoh
# filename: testzone
# Title: COM S 572 Lab 2

# file description
# this file is for testing only

# imports
from collections import namedtuple

# ______________________________________________________________________________
# testzone 

#_____________
# print board function

def printboard(board):
    for i in board:
        print(i)

#____________

# create 8x8 board
board = [["_" for j in range(0,8)] for i in range(0,8)]
# place white pieces
for i in range(0,3):
    if i %2 == 0:
        board[i] = ["_","B","_","B","_","B","_","B"]
    else:
        board[i] = ["B","_","B","_","B","_","B","_"]
# place black pieces
for i in range(len(board)-3,len(board)):
    if i %2 == 0:
        board[i] = ["_","W","_","W","_","W","_","W"]
    else:
        board[i] = ["W","_","W","_","W","_","W","_"]


printboard(board)

print("__________________________________________________________________________")
print("")
# ______________________________________________________________________________

GameState = namedtuple('GameState', 'to_move, utility, board, moves')
teststate = GameState(0, 1, 2, 3)

print("testing namedtuple")
print(teststate.to_move)
print(teststate.utility)
print(teststate.board)
print(teststate.moves)

print("__________________________________________________________________________")
print("")
# ______________________________________________________________________________

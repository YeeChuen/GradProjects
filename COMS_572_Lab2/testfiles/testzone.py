# Author: Yee Chuen Teoh
# filename: testzone
# Title: COM S 572 Lab 2

# file description
# this file is for testing only

# imports
from audioop import mul
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
        board[i] = ["_","W","_","W","_","W","_","W"]
    else:
        board[i] = ["W","_","W","_","W","_","W","_"]
# place black pieces
for i in range(len(board)-3,len(board)):
    if i %2 == 0:
        board[i] = ["_","B","_","B","_","B","_","B"]
    else:
        board[i] = ["B","_","B","_","B","_","B","_"]


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

playerdict={"1":["B","D"], "2":["W","V"]}

# COMPLETE checksimple
def checksimple(board, i,j):
    # check piece, 
    # piece type = W, B, V, D
    # V is king for W, D is king for B
    # i and j represent the location of the piece
    piece = board[i][j]

    # all simple move of the piece
    simplemoves = []

    # toplft = i-1, j-1
    # toprgt = i-1, j+1
    # btmlft = i+1, j-1
    # btmrgt = i+1, j+1
    top = i-1
    btm = i+1
    lft = j-1
    rgt = j+1

    if piece=="B" or piece=="D" or piece=="V":
        if top > -1:
            if lft > -1:
                if board[top][lft]=="_":
                    simplemoves.append([(i,j),(top,lft)])
                    # TO BE DELETED
                    #board[top][lft]="O"
            if rgt < len(board[0]):
                if board[top][rgt]=="_":
                    simplemoves.append([(i,j),(top,rgt)])
                    # TO BE DELETED
                    #board[top][rgt]="O"

    if piece=="W" or piece=="D" or piece=="V":
        if btm < len(board): 
            if lft > -1:
                if board[btm][lft]=="_":
                    simplemoves.append([(i,j),(btm,lft)])
                    # TO BE DELETED
                    #board[btm][lft]="O"
            if rgt < len(board[0]):
                if board[btm][rgt]=="_":
                    simplemoves.append([(i,j),(btm,rgt)])
                    # TO BE DELETED
                    #board[btm][rgt]="O"

    return simplemoves


# only does single jump
def checkjump(board, i,j):
    jumpmove=[]
    # check piece, 
    # piece type = W, B, V, D
    # V is king for W, D is king for B
    # i and j represent the location of the piece
    piece = board[i][j]
    # check oponent player
    if piece in playerdict["1"]:
        oponent = "2"
    else:
        oponent = "1"

    # toplft = i-1, j-1
    # toprgt = i-1, j+1
    # btmlft = i+1, j-1
    # btmrgt = i+1, j+1
    top = i-1
    btm = i+1
    lft = j-1
    rgt = j+1

    if piece=="B" or piece=="D" or piece=="V":
        if top > -1:
            if lft > -1:
                if board[top][lft] in playerdict[oponent]:
                    if top-1>-1 and lft-1>-1 and board[top-1][lft-1]=="_":
                        t=top-1
                        l=lft-1
                    # TO BE DELETED
                        #board[t][l]="C"
                        jumpmove.append([(i,j),(t,l)])
            if rgt < len(board[0]):
                if board[top][rgt] in playerdict[oponent]:
                    if top-1>-1 and rgt+1 < len(board[0]) and board[top-1][rgt+1]=="_":
                        t=top-1
                        r=rgt+1
                    # TO BE DELETED
                        #board[t][r]="C"
                        jumpmove.append([(i,j),(t,r)])

    if piece=="W" or piece=="D" or piece=="V":
        if btm < len(board): 
            if lft > -1:
                if board[btm][lft] in playerdict[oponent]:
                    if btm+1 < len(board) and lft-1>-1 and board[btm+1][lft-1]=="_":
                        b=btm+1
                        l=lft-1
                    # TO BE DELETED
                        #board[b][l]="C"
                        jumpmove.append([(i,j),(b,l)])
            if rgt < len(board[0]):
                if board[btm][rgt] in playerdict[oponent]:
                    if btm+1< len(board) and rgt+1< len(board[0]) and board[btm+1][rgt+1]=="_":
                        b=btm+1
                        r=rgt+1
                    # TO BE DELETED
                        #board[b][r]="C"
                        jumpmove.append([(i,j),(b,r)])

    if jumpmove:
        return multijump(board,jumpmove)
    
    print("no jumps available")
    return jumpmove


# if multiple jumps
'''
this function checks for multiple possible jumpmoves
- list parameter here is all the possible action 
'''
def multijump(board,actionlist):
    #TO BE DELETED initial list
    #print("initial list: " +str(actionlist))

    todelete = actionlist.copy()
    while todelete:
        # check if there is jump
        jump = False
        currlist = todelete.pop()
        # check the current piece that is performing this jump
        piece = board[currlist[0][0]][currlist[0][1]]
        # check oponent player
        if piece in playerdict["1"]:
            oponent = "2"
        elif piece in playerdict["2"]:
            oponent = "1"   
        else:
            print("inside function [multijump], piece invalid, unable to determine current player")
            #return

        # TO BE DELETED
        #print("checking piece in location: "+str(currlist[0][0]) +","+str(currlist[0][1]))
        #print("current piece symbol: "+piece)
        #print("looking at move: "+str(currlist))
        #print("current oponent: "+oponent)
        
        # i,j here are the location after taking the final jump in the list
        i=currlist[len(currlist)-1][0]
        j=currlist[len(currlist)-1][1]

        # TO BE DELETED
        #print("temp location {},{}".format(i,j))

        # check if the diagonal surrounding has pieces to jump to
        top = i-1
        btm = i+1
        lft = j-1
        rgt = j+1

        if piece=="B" or piece=="D" or piece=="V":
                if top > -1:
                    if lft > -1:
                        if board[top][lft] in playerdict[oponent]:
                            if top-1>-1 and lft-1>-1 and board[top-1][lft-1]=="_":
                                t=top-1
                                l=lft-1
                            # TO BE DELETED
                                #print("currently in IF 1")
                                #board[t][l]="C"

                                if (t,l) not in currlist:
                                    copylist=currlist.copy()
                                    copylist.append((t,l))
                                    actionlist.append(copylist)
                                    todelete.append(copylist)
                                    jump=True

                    if rgt < len(board[0]):
                        if board[top][rgt] in playerdict[oponent]:
                            if top-1>-1 and rgt+1 < len(board[0]) and board[top-1][rgt+1]=="_":
                                t=top-1
                                r=rgt+1
                            # TO BE DELETED
                                #print("currently in IF 2")
                                #board[t][r]="C"

                                if (t,r) not in currlist:
                                    copylist=currlist.copy()
                                    copylist.append((t,r))
                                    actionlist.append(copylist)
                                    todelete.append(copylist)
                                    jump=True

        if piece=="W" or piece=="D" or piece=="V":
                if btm < len(board): 
                    if lft > -1:
                        if board[btm][lft] in playerdict[oponent]:
                            if btm+1 < len(board) and lft-1>-1 and board[btm+1][lft-1]=="_":
                                b=btm+1
                                l=lft-1
                            # TO BE DELETED
                                #print("currently in IF 3")
                                #board[b][l]="C"

                                if (b,l) not in currlist:
                                    copylist=currlist.copy()
                                    copylist.append((b,l))
                                    actionlist.append(copylist)
                                    todelete.append(copylist)
                                    jump=True

                    if rgt < len(board[0]):
                        if board[btm][rgt] in playerdict[oponent]:
                            if btm+1 < len(board) and rgt+1 < len(board[0]) and board[btm+1][rgt+1]=="_":
                                b=btm+1
                                r=rgt+1
                            # TO BE DELETED
                                #print("currently in IF 4")
                                #board[b][r]="C"

                                if (b,r) not in currlist:
                                    copylist=currlist.copy()
                                    copylist.append((b,r))

                                    actionlist.append(copylist)
                                    todelete.append(copylist)
                                    jump=True
        
        if jump == True:
            actionlist.remove(currlist)

        # TO BE DELETED
        #print("current actionlist after loop:")
        #print(actionlist)    
        #print("current list length: {}".format(len(actionlist)))


    return actionlist


# testing function_
print("------------------ testing simplemove ------------------")
board = [["_","W","_","W","_","W","_","W"], 
["_","_","_","_","_","_","_","_"], 
["_","_","_","B","_","_","_","_"]]
printboard(board)
print("--- after checking move ---")
print("allowable moves: " + str(checksimple(board, len(board)-1,3)))
printboard(board)
print("------------------ testing simeple edge case for B ------------------")
board = [["B","_","_","B","_","_","_","B"], 
["B","_","_","B","_","_","_","B"], 
["B","_","_","_","B","_","_","B"]]
printboard(board)
for i in range (0, len(board)):
    for j in range (0, len(board[0])):
        if board[i][j] == "B":          
            print("allowable moves for B in {},{}: ".format(i,j) + str(checksimple(board, i,j)))
printboard(board)

print("------------------ testing simeple edge case for W ------------------")
board = [["W","_","_","W","_","_","_","W"], 
["W","_","_","W","_","_","_","W"], 
["W","_","_","_","W","_","_","W"]]
printboard(board)
for i in range (0, len(board)):
    for j in range (0, len(board[0])):
        if board[i][j] == "W":          
            print("allowable moves for B in {},{}: ".format(i,j) + str(checksimple(board, i,j)))
printboard(board)

print("------------------ testing jump for B ------------------")
board = [
["_","_","_","_","_","_","_","_"],
["_","_","_","_","_","_","_","_"], 
["_","_","_","W","_","V","_","_"],
["_","_","_","_","B","_","_","_"],
["_","_","_","W","_","W","_","_"], 
["_","_","_","_","_","_","_","_"], 
["_","_","_","_","_","_","_","_"], 
["_","_","_","_","_","_","_","_"]
]
printboard(board)
for i in range (0, len(board)):
    for j in range (0, len(board[0])):
        if board[i][j] == "B":          
            print("allowable moves for B in {},{}: ".format(i,j) + str(checkjump(board, i,j)))
printboard(board)

print("------------------ testing jump for W ------------------")
board = [
["_","_","_","_","_","_","_","_"],
["_","_","_","_","_","_","_","_"], 
["_","_","_","B","_","D","_","_"],
["_","_","_","_"," ","_","_","_"],
["_","_","_","B","_","B","_","_"], 
["_","_","_","_","_","_","_","_"], 
["_","_","_","_","_","_","_","_"], 
["_","_","_","_","_","_","_","_"]
]
printboard(board)
for i in range (0, len(board)):
    for j in range (0, len(board[0])):
        if board[i][j] == "W":          
            print("allowable moves for W in {},{}: ".format(i,j) + str(checkjump(board, i,j)))
printboard(board)

print("------------------ testing jump for D ------------------")
board = [
["_","_","_","_","_","_","_","_"],
["_","_","_","_","_","_","_","_"], 
["_","_","_","W","_","V","_","_"],
["_","_","_","_","D","_","_","_"],
["_","_","_","V","_","W","_","_"], 
["_","_","_","_","_","_","_","_"], 
["_","_","_","_","_","_","_","_"], 
["_","_","_","_","_","_","_","_"]
]
printboard(board)
for i in range (0, len(board)):
    for j in range (0, len(board[0])):
        if board[i][j] == "D":          
            print("allowable moves for D in {},{}: ".format(i,j) + str(checkjump(board, i,j)))
printboard(board)

print("------------------ testing jump for V ------------------")
board = [
["_","_","_","_","_","_","_","_"],
["_","_","_","_","_","_","_","_"], 
["_","_","_","D","_","B","_","_"],
["_","_","_","_","V","_","_","_"],
["_","_","_","B","_","D","_","_"], 
["_","_","_","_","_","_","_","_"], 
["_","_","_","_","_","_","_","_"], 
["_","_","_","_","_","_","_","_"]
]
printboard(board)
for i in range (0, len(board)):
    for j in range (0, len(board[0])):
        if board[i][j] == "V":          
            print("allowable moves for V in {},{}: ".format(i,j) + str(checkjump(board, i,j)))
printboard(board)

print("------------------ testing multi jump (when there is only 1 jump) ------------------")
board = [
["_","_","_","_","_","_","_","_"],
["_","_","_","_","_","_","_","_"], 
["_","_","_","W","_","_","_","_"],
["_","_","_","_","_","_","_","_"],
["_","_","_","V","_","_","_","_"], 
["_","_","_","_","_","_","_","_"], 
["_","_","_","W","_","_","_","_"], 
["_","_","_","_","B","_","_","_"]
]
printboard(board)
for i in range (0, len(board)):
    for j in range (0, len(board[0])):
        if board[i][j] == "B":     
            print("allowable moves for B in {},{}: ".format(i,j) + str(checkjump(board, i,j)))
printboard(board)

print("------------------ testing multi jump (when there is more than 1 jump) ------------------")
board = [
["_","_","_","_","_","_","_","_"],
["_","_","_","_","_","_","_","_"], 
["_","_","_","W","_","_","_","_"],
["_","_","_","_","_","_","_","_"],
["_","_","_","V","_","_","_","_"], 
["_","_","_","_","_","_","_","_"], 
["_","_","_","W","_","W","_","_"], 
["_","_","_","_","B","_","_","_"]
]
printboard(board)
for i in range (0, len(board)):
    for j in range (0, len(board[0])):
        if board[i][j] == "B":     
            print("allowable moves for B in {},{}: ".format(i,j) + str(checkjump(board, i,j)))   
printboard(board)

print("------------------ testing multi jump (complicated jumps) for B ------------------")
board = [
["_","W","_","W","_","_","_","W"],
["_","_","_","_","_","_","_","_"], 
["_","W","_","W","_","W","_","W"],
["_","_","_","_","_","_","_","_"],
["_","W","_","V","_","_","_","W"], 
["_","_","_","_","_","_","_","_"], 
["_","W","_","W","_","W","_","_"], 
["_","_","_","_","B","_","_","_"]
]
printboard(board)
for i in range (0, len(board)):
    for j in range (0, len(board[0])):
        if board[i][j] == "B":     
            print("allowable moves for B in {},{}: ".format(i,j) + str(checkjump(board, i,j)))    
printboard(board)

print("------------------ testing multi jump (complicated jumps) for D ------------------")
board = [
["_","W","_","W","_","_","_","W"],
["_","_","D","_","_","_","_","_"], 
["_","W","_","W","_","W","_","W"],
["_","_","_","_","_","_","_","_"],
["_","W","_","V","_","_","_","W"], 
["_","_","_","_","_","_","_","_"], 
["_","W","_","V","_","_","_","_"], 
["_","_","_","_","_","_","_","_"]
]
printboard(board)
for i in range (0, len(board)):
    for j in range (0, len(board[0])):
        if board[i][j] == "D":     
            print("allowable moves for D in {},{}: ".format(i,j) + str(checkjump(board, i,j)))    
printboard(board)

print("------------------ testing multi jump (complicated jumps) for D ------------------")
board = [
["_","W","_","W","_","_","_","W"],
["_","_","B","_","_","_","_","_"], 
["_","W","_","W","_","W","_","W"],
["_","_","_","_","_","_","_","_"],
["_","W","_","V","_","_","_","W"], 
["_","_","_","_","_","_","_","_"], 
["_","W","_","V","_","_","_","_"], 
["_","_","_","_","_","_","_","_"]
]
printboard(board)
for i in range (0, len(board)):
    for j in range (0, len(board[0])):
        if board[i][j] == "B":     
            print("allowable moves for B in {},{}: ".format(i,j) + str(checkjump(board, i,j)))    
printboard(board)

print("------------------ testing multi jump (complicated jumps) for D ------------------")
board = [
["_","D","_","D","_","D","_","_"],
["_","_","_","_","_","_","_","_"], 
["_","B","_","B","_","D","_","D"],
["_","_","_","_","V","_","_","_"],
["_","D","_","B","_","D","_","D"], 
["_","_","_","_","_","_","_","_"], 
["_","B","_","B","_","D","_","D"], 
["_","_","_","_","_","_","_","_"]
]
printboard(board)
for i in range (0, len(board)):
    for j in range (0, len(board[0])):
        if board[i][j] == "V":     
            print("allowable moves for V in {},{}: ".format(i,j) + str(checkjump(board, i,j)))    
printboard(board)
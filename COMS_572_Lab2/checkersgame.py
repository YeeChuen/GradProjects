# Author: Yee Chuen Teoh
# filename: checker game
# Title: COM S 572 Lab 2
# Reference: Search (Chapters 6) textbook Artificial Intelligence_ A Modern Approach
# Link: https://github.com/aimacode/aima-python

# file description
# this file contain the checkers game file

# imports
import copy
import itertools
import random
from collections import namedtuple
from sre_parse import State
import numpy as np
from utils import vector_add
import copy

# ______________________________________________________________________________
# MinMax Search


def minmax_decision(state, game):
    """Given a state in a game, calculate the best move by searching
    forward all the way to the terminal states. [Figure 5.3]"""

    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    # Body of minmax_decision:
    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))


# ______________________________________________________________________________


def expect_minmax(state, game):
    """
    [Figure 5.11]
    Return the best move for a player after dice are thrown. The game tree
	includes chance nodes along with min and max nodes.
	"""
    player = game.to_move(state)

    def max_value(state):
        v = -np.inf
        for a in game.actions(state):
            v = max(v, chance_node(state, a))
        return v

    def min_value(state):
        v = np.inf
        for a in game.actions(state):
            v = min(v, chance_node(state, a))
        return v

    def chance_node(state, action):
        res_state = game.result(state, action)
        if game.terminal_test(res_state):
            return game.utility(res_state, player)
        sum_chances = 0
        num_chances = len(game.chances(res_state))
        for chance in game.chances(res_state):
            res_state = game.outcome(res_state, chance)
            util = 0
            if res_state.to_move == player:
                util = max_value(res_state)
            else:
                util = min_value(res_state)
            sum_chances += util * game.probability(chance)
        return sum_chances / num_chances

    # Body of expect_minmax:
    return max(game.actions(state), key=lambda a: chance_node(state, a), default=None)


def alpha_beta_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_search:
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def alpha_beta_cutoff_search(oristate, origame, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    # TO BE DELETED
    #print(str(game.to_move(state)))

    newboard = copy.deepcopy(oristate.board)
    game=checkers(newboard, oristate.utility, oristate.to_move)
    state=game.initial
    player = game.to_move(state)
    print("bot player: {}".format(player))


    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
        # TO BE DELETED
        #print("test in main max_value")
        #print(game.printboard(state))

        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        # TO BE DELETED
        #print("test in main min_value")
        #print(game.printboard(state))

        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None

    for a in game.actions(state):
        # TO BE DELETED
        #print("test in main alpha_beta")
        #print(game.printboard(state))

        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a

    #TO BE DELETED
    #print(best_action)

    return best_action


# ______________________________________________________________________________
# Players for Games


def query_player(game, state):
    """Make a move by querying standard input."""
    print("current state:")
    game.printboard(state)
    moves = game.actions(state)

    # MODIFIED
    numberlist = []
    print("Available moves: ")
    for x in range(0,len(moves)):
        numberlist.append(x)
        print("{}: {}".format(str(x),str(moves[x])))

    # ORIGINAL CODE
    #print("available moves: {}".format(game.actions(state)))

    print("")
    move = input('Your move? ')
    while eval(move) not in numberlist:
        print("invalid move, please select move from available moves.")      
        move = input('Your new move? ')


    print("")
    return moves[eval(move)]


def random_player(game, state):
    """A player that chooses a legal move at random."""
    return random.choice(game.actions(state)) if game.actions(state) else None


def alpha_beta_player(game, state):
    return alpha_beta_search(state, game)


def minmax_player(game,state):
    return minmax_decision(state,game)


def expect_minmax_player(game, state):
    return expect_minmax(state, game)


# ______________________________________________________________________________
# Games state
GameState = namedtuple('GameState', 'to_move, utility, board, moves')

# ______________________________________________________________________________
# Checkers Game 
# MODIFIED

class checkers():

    # TO BE CHECK
    def __init__(self, board = [
        ["_","W","_","W","_","W","_","W"],
        ["W","_","W","_","W","_","W","_"], 
        ["_","W","_","W","_","W","_","W"],
        ["_","_","_","_","_","_","_","_"],
        ["_","_","_","_","_","_","_","_"], 
        ["B","_","B","_","B","_","B","_"], 
        ["_","B","_","B","_","B","_","B"], 
        ["B","_","B","_","B","_","B","_"]
        ], utility=0, to_move="1"):
        """Initial state of the chckers game"""
        # create 8x8 board
        # V as king for W
        # D as king for B
        self.board = board

        # total pices for W and B
        # D and V represent the kings for W and B
        self.piecesdict={}

        #dict for player's piece
        self.playerdict={"1":["B","D"], "2":["W","V"]}

        piece1=0
        piece2=0
        for i in range(0, len(board)):
            for j in range(0, len(board)):
                if board[i][j] in self.playerdict["1"]:
                    piece1+=1
                elif board[i][j] in self.playerdict["2"]:
                    piece2+=1
        self.piecesdict["1"]=piece1
        self.piecesdict["2"]=piece2

        # what is the initial state?
        # rule:  The player with the darker-coloured pieces moves first. - Wikipedia
        # Lab 1 require user to move first, hence, user will be dark, AI will be light
        # to_move indicate who's turn to move
        # moves indicate available move
        # TODO: utility, to_move, moves
        self.initial = GameState(to_move=to_move,
        utility=utility,
        board=self.board,
        moves= self.get_all_actions(self.board,"1"))
        # user go first (player) , AI go second

    # COMPLETE checksimple
    # MODIFICATION
    def checksimple(self, board, i,j):
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
    # MODIFICATION
    def checkjump(self, board, i,j):
        jumpmove=[]
        # check piece, 
        # piece type = W, B, V, D
        # V is king for W, D is king for B
        # i and j represent the location of the piece
        piece = board[i][j]
        # check oponent player
        if piece in self.playerdict["1"]:
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
                    if board[top][lft] in self.playerdict[oponent]:
                        if top-1>-1 and lft-1>-1 and board[top-1][lft-1]=="_":
                            t=top-1
                            l=lft-1
                        # TO BE DELETED
                            #board[t][l]="C"
                            jumpmove.append([(i,j),(t,l)])
                if rgt < len(board[0]):
                    if board[top][rgt] in self.playerdict[oponent]:
                        if top-1>-1 and rgt+1 < len(board[0]) and board[top-1][rgt+1]=="_":
                            t=top-1
                            r=rgt+1
                        # TO BE DELETED
                            #board[t][r]="C"
                            jumpmove.append([(i,j),(t,r)])

        if piece=="W" or piece=="D" or piece=="V":
            if btm < len(board): 
                if lft > -1:
                    if board[btm][lft] in self.playerdict[oponent]:
                        if btm+1 < len(board) and lft-1>-1 and board[btm+1][lft-1]=="_":
                            b=btm+1
                            l=lft-1
                        # TO BE DELETED
                            #board[b][l]="C"
                            jumpmove.append([(i,j),(b,l)])
                if rgt < len(board[0]):
                    if board[btm][rgt] in self.playerdict[oponent]:
                        if btm+1< len(board) and rgt+1< len(board[0]) and board[btm+1][rgt+1]=="_":
                            b=btm+1
                            r=rgt+1
                        # TO BE DELETED
                            #board[b][r]="C"
                            jumpmove.append([(i,j),(b,r)])

        if jumpmove:
            return self.multijump(board,jumpmove)
        
        #print("no jumps available")
        return jumpmove


    # if multiple jumps
    # MODIFICATION
    '''
    this function checks for multiple possible jumpmoves
    - list parameter here is all the possible action 
    '''
    def multijump(self, board,actionlist):
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
            if piece in self.playerdict["1"]:
                oponent = "2"
            elif piece in self.playerdict["2"]:
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
                            if board[top][lft] in self.playerdict[oponent]:
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
                            if board[top][rgt] in self.playerdict[oponent]:
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
                            if board[btm][lft] in self.playerdict[oponent]:
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
                            if board[btm][rgt] in self.playerdict[oponent]:
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

    # get_all_actions is for GameState, similar code with self.actions
    def get_all_actions(self, board, to_move):
        """Return a list of the allowable moves at this point."""
        """
        actions will be lists of lists of tuples
        tuples stores the coordinate on the board which represent the moves, 
        each list in the mainlist represent each available moves.
        return a list that stores a lists of available moves
        """
        jumpmove = []
        simplemove = []

        currplayer = to_move

        # TO BE DELETED
        #print("inside get_all_action function")

        board = board

        for i in range(0,len(board)):
            for j in range(0,len(board[0])):
                if board[i][j] in self.playerdict[currplayer]:
                    jumpmove += self.checkjump(board,i,j)
                    if not jumpmove:
                        simplemove+=self.checksimple(board,i,j)

        if jumpmove:
            return jumpmove
        else:
            return simplemove

    # TO BE CHECK
    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        """
        actions will be lists of lists of tuples
        tuples stores the coordinate on the board which represent the moves, 
        each list in the mainlist represent each available moves.
        return a list that stores a lists of available moves
        """
        jumpmove = []
        simplemove = []

        currplayer = state.to_move

        # TO BE DELETED
        #print("inside action function")

        board = state.board

        for i in range(0,len(board)):
            for j in range(0,len(board[0])):
                if board[i][j] in self.playerdict[currplayer]:
                    jumpmove += self.checkjump(board,i,j)
                    if not jumpmove:
                        simplemove+=self.checksimple(board,i,j)

        if jumpmove:
            return jumpmove
        else:
            return simplemove

    # TO BE CHECK
    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        """selected move will be a list of tuples where tuples is the """
        currplayer = state.to_move
        board = state.board
        piece_to_move=board[move[0][0]][move[0][1]]
        board[move[0][0]][move[0][1]] = "_"

        for x in range(0,len(move)-1):
            tuple1=move[x]
            tuple2=move[x+1]
            #btm for neg
            if tuple2[0]-tuple1[0] < 0:
                i = tuple1[0]+(tuple2[0]-tuple1[0]+1)
            elif tuple2[0]-tuple1[0] > 0:
                i = tuple1[0]+(tuple2[0]-tuple1[0]-1)
            if tuple2[1]-tuple1[1] < 0:
                j = tuple1[1]+(tuple2[1]-tuple1[1]+1)
            elif tuple2[1]-tuple1[1] > 0:
                j = tuple1[1]+(tuple2[1]-tuple1[1]-1)

            # TO BE DELETED
            #print("{},{}".format(i,j))

            board[i][j]="_"

        finaltuple = move[len(move)-1]
        if finaltuple[0]==0 or finaltuple[0]==len(board)-1:
            if piece_to_move=="B" or piece_to_move=="D":
                board[finaltuple[0]][finaltuple[1]]="D"
            if piece_to_move=="W" or piece_to_move=="V":
                board[finaltuple[0]][finaltuple[1]]="V"
        else:
            board[finaltuple[0]][finaltuple[1]]=piece_to_move

        # DONE: Calculate the pieces left
        piece1=0
        piece2=0
        for i in range(0, len(board)):
            for j in range(0, len(board)):
                if board[i][j] in self.playerdict["1"]:
                    piece1+=1
                elif board[i][j] in self.playerdict["2"]:
                    piece2+=1
        self.piecesdict["1"]=piece1
        self.piecesdict["2"]=piece2

        # TO BE DELETED
        # print("pieces on board after move for player 1: {} , player 2: {}".format(self.piecesdict["1"], self.piecesdict["2"]))
        #self.initial = GameState(to_move=("2" if currplayer =="1" else "1"), utility=0, board=board, moves= self.actions)

        return GameState(to_move=("2" if currplayer =="1" else "1"),
        utility=self.compute_utility(board, currplayer),
        board=board,
        moves=self.get_all_actions(board,("2" if currplayer =="1" else "1")))

    def compute_utility(self, board, player):
        """If '2' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        #TO BE DELETED
        #print("inside compute_utility")

        if player == "1":
            oponent ="2"
        elif player =="2":
            oponent ="1"

        # reward points when oponent have no pieces left or there is no move from oponent
        # the next turn is oponent's turn, check action for oponent's piece
        if self.piecesdict[oponent]==0 or not self.get_all_actions(board,oponent):
            if player =="2":
                #TO BE DELETED
                #print("compute_utility with reward for player 2")
                return 1
            else:
                #TO BE DELETED
                #print("compute_utility with deduction for player 2")
                return -1
        else:
            #TO BE DELETED
            #print("end compute_utility with 0")

            return 0

    def utility(self, state, player):
        """Return the value of this final state to player."""
        # TODO
        #TO BE DELETED
        #print("inside utility")
        #print("looking at player {}".format(player))

        return state.utility if player == "2" else -state.utility

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        # TODO
        
        # TO BE DELETED
        #if not self.actions(state):
            #print("no actions left")
        #elif self.piecesdict["1"]==0:
            #print("no pieces left for player 1")
        #elif self.piecesdict["2"]==0:
            #print("no pieces left for player 2")
        #if self.utility(state, self.to_move(self.initial))!=0:
            #print(self.utility(state, self.to_move(self.initial)))
            #print("player 2 is awarded or deducted point")

        return not self.actions(state) or self.piecesdict["1"]==0 or self.piecesdict["2"]==0 or self.utility(state, self.to_move(self.initial))!=0

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        # TODO
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        # TODO
        # ignore for now

        # below is original code only contain print(state)
        #print(state)

        #MODIFIED
        #print("display function is being run")

        board = state.board
        print(["_","0","1","2","3","4","5","6","7"])
        count=[0]
        for list in board:
            print("  "+str(count)+str(list))
            count[0]+=1

    def __repr__(self):
        # TODO :  check what is this
        # ignore for now
        return '<{}>'.format(self.__class__.__name__)

    # ignore play_game function
    def play_game(self, *players):
        # TODO :  check what is this
        """Play an n-person, move-alternating game."""
        state = self.initial

        # TO BE DELETED
        count=0

        # TO BE DELETED
        #print(players)

        while True:
            for player in players:
                count+=1
                # TODO: the if statement conditional need to be modified again
                # TODO: conditional to 1000 so it wont run
                if len(player)==1000:
                    print("-------------------------------- checkpoint(each turn) ROUND {} --------------------------------".format(str (count)))
                    # TO BE DELETED
                    print("currently player {}'s turn".format(state.to_move))
                    #moves = self.actions(state)
                    moves = state.moves
                    self.printboard(state)
                    #print(moves)
                    print("available moves are: ")
                    for x in range(0,len(moves)):
                        print("{}: {}".format(str(x),str(moves[x])))
                    # uncomment below for player to play
                    #userchoice = input()
                    # change moves[0] to moves[int(userchoice)] for enable player to play
                    print("chosen move {}: {}".format(str(0),str(moves[0])))
                    state = self.result(state, moves[0])

                else:
                    print("-------------------------------- checkpoint(each turn) ROUND {} --------------------------------".format(str (count)))
                  
                    # TO BE DELETED
                    print("inside play_game's else statement FOR ALPHA BETA")

                    # TODO: below is original
                    move = player(self, state)
                    # TODO: below is original
                    state = self.result(state, move)

                if self.terminal_test(state):
                    # TO BE DELETED
                    #print("inside play_game 's terminal_test if statement")

                    self.display(state)
                    print("current player {} score: {}".format(self.to_move(self.initial),str(self.utility(state, self.to_move(self.initial)))))
                    return self.utility(state, self.to_move(self.initial))

    # test play game with two player
    def play_game_twoplayer(self):
        # TODO :  check what is this
        """Play an n-person, move-alternating game."""
        state = self.initial

        # TO BE DELETED
        count=0

        # TO BE DELETED
        print("start game")

        while True:
                count+=1
                # TODO: the if statement conditional need to be modified again
                # TODO: conditional to 1000 so it wont run
                print("-------------------------------- checkpoint(each turn) ROUND {} --------------------------------".format(str (count)))
                  
                # TO BE DELETED
                print("2 player game, currently its player {}'s turn".format(state.to_move))

                # TODO: below is original
                move = query_player(self, state)
                # TODO: below is original
                state = self.result(state, move)

                if self.terminal_test(state):
                    # TO BE DELETED
                    #print("inside play_game 's terminal_test if statement")

                    self.display(state)

                    #TO BE DELETED
                    currplayer = state.to_move
                    secondplayer = ""
                    if currplayer == "1":
                        secondplayer ="2"
                    elif currplayer =="2":
                        secondplayer="1"

                    print("current player {} score: {}".format(currplayer,str(self.utility(state, currplayer))))

                    print("current player {} score: {}".format(secondplayer,str(self.utility(state, secondplayer))))
                    
                    return self.utility(state, self.to_move(self.initial))

    # test play game with only 1 player
    # test play game with two payer
    # TODO: fix so that the search dont finish the game 
    def play_game_oneplayer(self):
        # TODO :  check what is this
        """Play an n-person, move-alternating game."""
        state = self.initial

        # TO BE DELETED
        count=0

        # TO BE DELETED
        print("start game")
        print("human = Player 1, AI = Player 2")

        while True:
            for turn in range(0,2):
                count+=1
                # TODO: the if statement conditional need to be modified again
                # TODO: conditional to 1000 so it wont run
                print("-------------------------------- checkpoint(each turn) ROUND {} --------------------------------".format(str (count)))
                  
                # TO BE DELETED
                print("1 player game, currently its player {}'s turn".format(state.to_move))

                if turn == 0:
                    # TODO: below is original
                    move = query_player(self, state)
                    # TODO: below is original
                    state = self.result(state, move)

                elif turn == 1:
                    # TODO: below is original
                    move = alpha_beta_cutoff_search(state, self, 100)

                    # TO BE DELETED
                    self.printboard(state)
                    print("AI chose move: {}".format(str(move)))

                    # TODO: below is original
                    state = self.result(state, move)

                if self.terminal_test(state):
                    # TO BE DELETED
                    #print("inside play_game 's terminal_test if statement")

                    self.display(state)

                    #TO BE DELETED
                    currplayer = state.to_move
                    secondplayer = ""
                    if currplayer == "1":
                        secondplayer ="2"
                    elif currplayer =="2":
                        secondplayer="1"

                    print("current player {} score: {}".format(currplayer,str(self.utility(state, currplayer))))

                    print("current player {} score: {}".format(secondplayer,str(self.utility(state, secondplayer))))
                    
                    return self.utility(state, self.to_move(self.initial))

    # the AI vs AI
    def play_game_AI(self):
        # TODO :  check what is this
        """Play an n-person, move-alternating game."""
        state = self.initial

        # TO BE DELETED
        count=0

        # TO BE DELETED
        print("start game")
        print("human = Player 1, AI = Player 2")

        while True:
            for turn in range(0,2):
                count+=1
                # TODO: the if statement conditional need to be modified again
                # TODO: conditional to 1000 so it wont run
                print("-------------------------------- checkpoint(each turn) ROUND {} --------------------------------".format(str (count)))
                  
                # TO BE DELETED
                print("AI vs AI game, currently its player {}'s turn".format(state.to_move))

                if turn == 0:
                    #print("---------------------------------- this run 1 ----------------------------------")
                    # TODO: below is original
                    move = alpha_beta_cutoff_search(state, self, 100)

                    # TO BE DELETED
                    self.printboard(state)
                    print("AI chose move: {}".format(str(move)))
                    
                    # TODO: below is original
                    state = self.result(state, move)

                elif turn == 1:
                    #print("---------------------------------- this run 2 ----------------------------------")
                    # TODO: below is original
                    move = alpha_beta_cutoff_search(state, self)

                    # TO BE DELETED
                    self.printboard(state)
                    print("AI chose move: {}".format(str(move)))
                    
                    # TODO: below is original
                    state = self.result(state, move)

                if self.terminal_test(state):
                    # TO BE DELETED
                    #print("inside play_game 's terminal_test if statement")

                    self.display(state)

                    #TO BE DELETED
                    currplayer = state.to_move
                    secondplayer = ""
                    if currplayer == "1":
                        secondplayer ="2"
                    elif currplayer =="2":
                        secondplayer="1"

                    print("current player {} score: {}".format(currplayer,str(self.utility(state, currplayer))))

                    print("current player {} score: {}".format(secondplayer,str(self.utility(state, secondplayer))))
                    
                    return self.utility(state, self.to_move(self.initial))



    # TO BE DELETED
    def printboard(self, state):
        board = state.board
        print(["_","0","1","2","3","4","5","6","7"])
        count=[0]
        for list in board:
            print("  "+str(count)+str(list))
            count[0]+=1
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
from COMS_572_Lab2.testzone import checkjump
from utils import vector_add

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


def alpha_beta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta, depth):
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
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


# ______________________________________________________________________________
# Players for Games


def query_player(game, state):
    """Make a move by querying standard input."""
    print("current state:")
    game.display(state)
    print("available moves: {}".format(game.actions(state)))
    print("")
    move = None
    if game.actions(state):
        move_string = input('Your move? ')
        try:
            move = eval(move_string)
        except NameError:
            move = move_string
    else:
        print('no legal moves: passing turn to next player')
    return move


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
    def __init__(self):
        """Initial state of the chckers game"""
        # create 8x8 board
        # V as king for W
        # D as king for B
        board = [
        ["_","W","_","W","_","W","_","W"],
        ["W","_","W","_","W","_","W","_"], 
        ["_","W","_","W","_","W","_","W"],
        ["_","_","_","_","_","_","_","_"],
        ["_","_","_","_","_","_","_","_"], 
        ["B","_","B","_","B","_","B","_"], 
        ["_","B","_","B","_","B","_","B"], 
        ["B","_","B","_","B","_","B","_"]
        ]

        # total pices for W and B
        self.Bpieces = 12
        self.Wpieces = 12
        # D and V represent the kings for W and B
        self.Dpieces = 0
        self.Vpieces = 0

        #dict for player's piece
        self.playerdict={"1":["B","D"], "2":["W","V"]}

        # what is the initial state?
        # rule:  The player with the darker-coloured pieces moves first. - Wikipedia
        # Lab 1 require user to move first, hence, user will be dark, AI will be light
        # to_move indicate who's turn to move
        # moves indicate available move
        # TODO: utility, to_move, moves
        self.initial = GameState(to_move='1', utility=0, board=board, moves= self.actions)
        # user go first (player) , AI go second

    # COMPLETE checksimple
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
    def checkjump(self, board, i,j):
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

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        """selected move will be a list of tuples where tuples is the """
        
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))
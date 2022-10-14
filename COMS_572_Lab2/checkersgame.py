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
import numpy as np
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

    def __init__(self):
        """Initial state of the chckers game"""
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

        # what is the initial state?
        # rule:  The player with the darker-coloured pieces moves first. - Wikipedia
        # TODO: utility, to_move, moves
        self.initial = GameState(to_move='B', utility=0, board=board, moves=moves)
        # user go first (player) , AI go second

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
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
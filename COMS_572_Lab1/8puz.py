#Author: Yee Chuen Teoh
#Title: COM S 572 Lab 1
#Reference: Search (Chapters 3-4) textbook Artificial Intelligence_ A Modern Approach

import argparse
from time import time
from Pformulation import *
from search import *
import time

#choose time limit for each algo
'''Edit minimum time here
currently set at 10'''
mintime = 10

'''
NOTES
- MUST DO current overtime using is 120s to be change to 900s
- MUST DO how to read/access folder
- MUST DO make it so it can run all files at once
'''

#create parser
parser = argparse.ArgumentParser()
#add parser argument --fPath and --alg and --alltxt

#choose a txt file to run, needs to be in same folder
#example --fPath S1.txt
#type all to run all txt file
parser.add_argument('--fPath', type=str, required=True)

#choose a algorithm to run
#example --alg BFS/IDS/h1/h2/h3
#type all to run all 5 algorithm, --alg all
parser.add_argument('--alg', type=str, required=True)

#parse the argument
args = parser.parse_args()

#check what algo is asked to run
algo = args.alg

#a function to help printing
def printresult(search, starttime):
    endtime = time.time()
    if search == None:
        print("search algo failed")

    elif search.state == "Timed out.":
        print("Total nodes generated: <<??>>")
        print("Total time taken: >15 min")
        print("Path length: "+search.state)
        print("Path: "+search.state)

        
    else:
        print("Total nodes generated: "+str(search.nodeNum))
        print("Total time taken: "+str(endtime-starttime)+"seconds")
        print("Path length: "+str(search.path_cost))
        print("Path: "+''.join(search.solution()))

#get the txt file, convert to initialstate form
contents = args.fPath
puzzlefile = open(contents, "r")
puzzle = puzzlefile.read()
a = puzzle.replace(" ","")
initialstate = a.replace("\n","")
#create the problem using initial state
problem = EightPuzzle(initialstate)

#check problem solvability
print(contents+" solvability")
print(problem.check_solvability(initialstate))

if not problem.check_solvability(initialstate):
    print("The inputted puzzle is not solvable:")
    print(puzzle)

else:
 
    #BFS
    if algo == "BFS" or algo == "all":
        starttime = time.time()
        print(contents+" on BFS ---")
        printresult(breadth_first_graph_search(problem, starttime, mintime), starttime)

    #IDS
    '''
    note: nodes generated in IDS is much higher
    as nodes in every depth limit is counted as generated,
    and not just only when the solution is found.
    '''
    if algo == "IDS" or algo == "all":
        starttime = time.time()
        print(contents+" on IDS ---")
        printresult(iterative_deepening_search(problem, starttime, mintime), starttime)

    #h1
    if algo == "h1" or algo == "all":
        starttime = time.time()
        print(contents+" on h1 ---")
        problem = EightPuzzleH1(initialstate)
        printresult(astar_search(problem, starttime, mintime), starttime)

    #h2
    if algo == "h2" or algo == "all":
        starttime = time.time()
        print(contents+" on h2 ---")
        problem = EightPuzzleH2(initialstate)
        printresult(astar_search(problem, starttime, mintime), starttime)

    #h3
    if algo == "h3" or algo == "all":
        starttime = time.time()
        print(contents+" on h3 ---")
        problem = EightPuzzleH3(initialstate)
        printresult(astar_search(problem, starttime, mintime), starttime)



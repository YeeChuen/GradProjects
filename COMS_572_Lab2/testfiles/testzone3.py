# Author: Yee Chuen Teoh
# Title: testzone3


from checkersgame import *
from time import time
import time

game = checkers()
print("currently playing: ")
print(game.__repr__())


print("Game Types: ")
print("[1] two player")
print("[2] one player vs AI")
print("[3] AI vs AI")
print("[4] test eval")

valid =[1,2,3,4]
choice = input("select game type: ")
while int(choice) not in valid:
    choice = input("select a valid game type: ")


# two player
if int(choice) == 1:
    game.play_game_twoplayer()

# one player vs AI
elif int(choice) == 2:
    level =["E","M","H", "R"]
    print("AI level: ")
    print("[E] Easy AI")
    print("[M] Medium AI")
    print("[H] Hard AI")
    print("[R] Random AI")
    lvlchoice = input("select AI level: ")
    while str(lvlchoice) not in level:
        lvlchoice = input("select a valid AI level: ")

    if str(lvlchoice) != "R":
        print("input depth level 1 to 100:")
        print("0 < d < 11")
        d = input("select depth level: ")
        while int(d) < 1 or int(d) > 10 :
            lvlchoice = input("select a valid depth level between 1 to 100: ")

    print("AI level selected = {}".format(str(lvlchoice)))
    print("AI depth selected = {}".format(str(d)))

    game.play_game_oneplayer(str(lvlchoice), int(d))

    print("AI level selected = {}".format(str(lvlchoice)))
    print("AI depth selected = {}".format(str(d)))

# AI vs AI
elif int(choice) == 3:
    level =["E","M","H", "R"]
    print("AI level for AI player 1: ")
    print("[E] Easy AI")
    print("[M] Medium AI")
    print("[H] Hard AI")
    print("[R] Random AI")
    AIlvl1 = input("select AI level: ")
    while str(AIlvl1) not in level:
        AIlvl1 = input("select a valid AI level: ")
        
    if str(AIlvl1) != "R":
        print("input depth level 1 to 100 for AI player 1:")
        print("0 < d < 11")
        d1 = input("select depth level: ")
        while int(d1) < 1 or int(d1) > 10 :
            d1 = input("select a valid depth level between 1 to 100: ")


    print("")
    print("AI level for AI player 2: ")
    print("[E] Easy AI")
    print("[M] Medium AI")
    print("[H] Hard AI")
    print("[R] Random AI")
    AIlvl2 = input("select AI level: ")
    while str(AIlvl2) not in level:
        AIlvl2 = input("select a valid AI level: ")
        
    if str(AIlvl2) != "R":
        print("input depth level 1 to 100 for AI player 1:")
        print("0 < d < 11")
        d2 = input("select depth level: ")
        while int(d2) < 1 or int(d2) > 10 :
            d2 = input("select a valid depth level between 1 to 100: ")

        
    print("AI player 1 level selected = {}".format(str(AIlvl1)))
    print("AI player 1 depth selected = {}".format(str(d1)))
    print("AI player 2 level selected = {}".format(str(AIlvl2)))
    print("AI player 2 depth selected = {}".format(str(d2)))

    gamestart = time.time()
    game.play_game_AI(str(AIlvl1),int(d1), str(AIlvl2), int(d2))
    gameend = time.time()

    print("Total game time: {}".format(str(round(gameend-gamestart, 5))))
    print("AI player 1(B/D) level selected = {}".format(str(AIlvl1)))
    print("AI player 1(B/D) depth selected = {}".format(str(d1)))
    print("AI player 2(W/V) level selected = {}".format(str(AIlvl2)))
    print("AI player 2(W/V) depth selected = {}".format(str(d2)))

# AI vs AI
elif int(choice) == 4:
    print("Welcome to test zone")
    print("Testing Eval Function")
    print("To modify Eval Function please go to checkersgame")
    print("Enter anything to start testing")

    gamestart = time.time()
    game.play_game_test()
    gameend = time.time()
    print("Total game time: {}".format(str(round(gameend-gamestart, 5))))

print("")
print("--- end checkers ---")
# Author: Yee Chuen Teoh
# Title: testzone3


from checkersgame import *


game = checkers()
print("currently playing: ")
print(game.__repr__())


print("Game Types: ")
print("[1] two player")
print("[2] one player vs AI")
print("[3] AI vs AI")

valid =[1,2,3]
choice = input("select game type: ")
while eval(choice) not in valid:
    choice = input("select a valid game type: ")


# two player
if eval(choice) == 1:
    game.play_game_twoplayer()

# one player vs AI
elif eval(choice) == 2:
    game.play_game_oneplayer()

# AI vs AI
elif eval(choice) == 3:
    game.play_game_AI()

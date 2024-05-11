'''
library for the entropy game from https://www.codecup.nl/entropy/rules.php

Board
The gameboard is a square grid of 7x7 cells. A match between two players consists of two games. 
Each game starts with the board empty, and a bag containing 49 chips in seven colours.  
The first player to move (Chaos) draws coloured chips at random from the bag and places each one on the board in an empty cell. 
For each chip that is placed, the second player (Order) may slide any chip horizontally or vertically any distance through empty cells, 
to rest in a currently empty cell. When the board becomes full, the game is finished.

Order scores 1 point for each chip in any palindromic pattern of chip colours
occurring either horizontally or vertically. The players reverse roles and play a second game. 
The player with the higher score is the better player.

Input/output
A communication protocol has been designed for your program to communicate with the judging software.

If your player is Chaos, the first line you will read is "Start". Your program must first read the colour 
of the first chip and then must output the first move. An example of a move is Bc, the first letter is the 
row, the second is the column. The chips come in random order. If the first line you will read is something 
like 3Bc, then your player is Order. That means Chaos was given colour 3 and he placed it on spot Bc. 
The colours are numbered from 1 to 7. Then you must slide one of your chips vertically or horizontally, 
for the first chip you can do something like BcBg, although BcBc is also allowed. After this your program 
must read the move of the other player and must continue responding with their own move until they receive "Quit" as input.

Note that Chaos always reads the colour of the next chip before he can output the next move. When there are no moves left to 
play, you will receive one final "Quit" instruction. If your program makes an illegal move you will be sent a "Quit" 
instruction as well. This should allow you to send debugging information to standard error.
'''

import random
import sys

class TreeMinMax:
    def __init__(self, game, color = None):
        self.game = game
        self.currentColor = color
        self.root = Node(self.game, self.currentColor)
        self.best = self.root
        self.best_score = -10000

class Colors_game:
    def __init__(self):
        self.stack = [i%7 + 1 for i in range(49)]
        random.shuffle(self.stack)
    
    def get_color(self):
        return self.stack[-1]

    def next_color(self):
        return self.stack.pop()



class Colors_bot:
    def __init__(self):
        self.list = [7 for i in range(7)]
    
    def remove_color(self, color): #cores: 0 - 6
        self.list[color] -= 1


class Board:
    def __init__(self):
        self.state = [[0 for _ in range(7)] for _ in range(7)]

class Chaos:
    def __init__(self, game, color = None):
        self.currentColor = color
        self.game = game
    
    def move(self, color):
        self.currentColor = color
        #jogada aq#
        return self.game.order.move(color)


class Order:
    def __init__(self, game, color = None):
        self.game = game

    def move(self, color):
        if color == 'Quit':
            return 'Quit'
        #jogada aq#

        

        return self.game.chaos.move(color)

class Entropy:
    def __init__(self):
        self.board = Board()
        self.order = Order(self)
        self.chaos = Chaos(self)

def eval():
    return 1

def main():
    game = Entropy()
    start = sys.stdin.readline()
    if start == 'Start':
        chaos_move = sys.stdin.readline()
        game.chaos.move(chaos_move)
    else:
        game.order.move(start)

if __name__ == '__main__':
    main()

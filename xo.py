#!/usr/bin/env python3
# https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python/

from argparse import ArgumentParser
from os import system, name 

clear = "cls" if name == 'nt' else "clear"
alpha_beta_pruning = True

class Game:
    def __init__ (self):
        self.initialize_board()

    def initialize_board(self):    
        self.board = [['.','.','.'],['.','.','.'],['.','.','.'],]
        self.player_turn = 'X'
    
    def draw_board(self):
        print("=========================")
        print("||      TicTacToe      ||")
        print("=========================")
        print("||       1   2   3     ||")
        print("||                     ||")
        print("|| 1   ", " {} ¦ {} ¦ {} ".format(self.board[0][0], self.board[0][1], self.board[0][2]), "   ||")
        print("||      ---+---+---    ||")
        print("|| 2   ", " {} ¦ {} ¦ {} ".format(self.board[1][0], self.board[1][1], self.board[1][2]), "   ||")
        print("||      ---+---+---    ||")
        print("|| 3   ", " {} ¦ {} ¦ {} ".format(self.board[2][0], self.board[2][1], self.board[2][2]), "   ||")
        print("||                     ||")
        print("=========================")

    def is_valid(self, x, y):
        if x in range(3) and y in range(3):
            if self.board[x][y] == '.':
                return True
        return False

    def is_end(self):
        # horizontal
        for i in range(3):
            if (self.board[i] == ['X','X','X']):
                return 'X'
            elif (self.board[i] == ['O','O','O']):
                return 'O'
        
        # vertical
        for i in range(3):
            if (self.board[0][i] != '.' and
                self.board[0][i] == self.board[1][i] and
                self.board[1][i] == self.board[2][i]):
                return self.board[0][i]
        
        # diagonal
        if (self.board[0][0] != '.' and
            self.board[0][0] == self.board[1][1] and
            self.board[0][0] == self.board[2][2]):
            return self.board[0][0]        
        if (self.board[0][2] != '.' and
            self.board[0][2] == self.board[1][1] and
            self.board[0][2] == self.board[2][0]):
            return self.board[0][2]   

        # not yet finished
        for i in range(0, 3):
            for j in range(0, 3):
                if (self.board[i][j] == '.'):
                    return None

        # tie
        return '.'
    
    # maximizing for O
    def max(self):
        # print("+", end="")
        maxv = -2
        px = None
        py = None
        
        # payoffs: loss = -1, tie = 0, win = 1
        result = self.is_end()
        if result == 'X':
            return (-1,0,0)
        elif result == 'O':
            return (1,0,0)
        elif result == '.':
            return (0,0,0)

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '.':
                    self.board[i][j] = 'O'
                    (m, _, _) = self.min()
                    if m > maxv:
                       maxv = m
                       px = i
                       py = j
                    # restore the board
                    self.board[i][j] = '.'
        return (maxv, px, py)

    # maximizing for O with alpha-beta-pruning
    def max_abp(self, alpha, beta):
        # print("+", end="")
        maxv = -2
        px = None
        py = None
        
        # payoffs: loss = -1, tie = 0, win = 1
        result = self.is_end()
        if result == 'X': return (-1,0,0)
        elif result == 'O': return (1,0,0)
        elif result == '.': return (0,0,0)

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '.':
                    self.board[i][j] = 'O'
                    (m, _, _) = self.min_abp(alpha,beta)
                    if m > maxv:
                       maxv = m
                       px = i
                       py = j
                    # restore the board
                    self.board[i][j] = '.'

                    # alpha beta pruning
                    if maxv >= beta:
                        return(maxv, px, py)
                    if maxv > alpha:
                        alpha = maxv

        return (maxv, px, py)

    # minimizing for X
    def min(self):
        # print("-", end="")
        minv = 2
        qx = None
        qy = None

        # payoffs: loss = 1, tie = 0, win = -1
        result = self.is_end()

        if result == 'X':
            return (-1,0,0)
        elif result == 'O':
            return (1,0,0)
        elif result == '.':
            return (0,0,0)

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '.':
                    self.board[i][j] = 'X'
                    (m, _, _) = self.max()
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    # restore board
                    self.board[i][j] = '.'

        return(minv, qx, qy)
   
    # minimizing for X with alpha-beta-pruning
    def min_abp(self, alpha, beta):
        # print("-", end="")
        minv = 2
        qx = None
        qy = None

        # payoffs: loss = 1, tie = 0, win = -1
        result = self.is_end()

        if result == 'X':
            return (-1,0,0)
        elif result == 'O':
            return (1,0,0)
        elif result == '.':
            return (0,0,0)

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '.':
                    self.board[i][j] = 'X'
                    (m, _, _) = self.max_abp(alpha, beta)
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    # restore board
                    self.board[i][j] = '.'

                    # alpha-beta-pruning
                    if minv <= alpha:
                        return (minv,qx,qy)
                    if minv < beta:
                        beta = minv

        return(minv, qx, qy)
   
    # game loop
    def play(self):

        while True:
            self.draw_board()
            print()
            self.result = self.is_end()
            if self.result != None:
                if self.result == '.':
                   print("It's a tie!")
                else:
                    print("The Winner is ", self.result)
                self.initialize_board()
                return
                
            # Player turn
            if self.player_turn == 'X':
                print("Player turn")
                while True:
                    if alpha_beta_pruning:
                        (m, qx, qy) = self.min_abp(-2,2)
                    else:
                        (m, qx, qy) = self.min()

                    print('Recommended move: X = {}, Y = {}'.format(qx+1, qy+1))

                    px = int(input('Insert X coordinate: '))-1
                    py = int(input('Insert Y coordinate: '))-1
                    
                    (qx, qy) = (px, py)
                    
                    if self.is_valid(px, py):
                        self.board[px][py] = 'X'
                        self.player_turn = 'O'
                        break
                    else: 
                        print("Not a valid move")
                        print("Try again, frend :^)")
                        print()
            # AI turn
            else:
                print("AI is thinking...")
                if alpha_beta_pruning:
                    (m, px, py) = self.max_abp(-2,2)
                else:
                    (m, px, py) = self.max()
                self.board[px][py] = 'O'
                print("AI did a thing")
                self.player_turn = 'X'
                
            #system(clear) #system(("clear", "cls")[name == 'nt'])

def main():
    Game().play()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--pruning', dest='abp', action='store_true')
    parser.add_argument('--no-pruning', dest='abp', action='store_false')
    parser.set_defaults(abp=True)
    args = parser.parse_args()
    
    alpha_beta_pruning = args.abp
    main()

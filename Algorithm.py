import random
import sys

import pygame


class Human:
    def __init__(self, name='Human'):
        self.name = name
        self.win = 0
        self.lose = 0
        self.point = 0
        self.tie = 0
        self.match = 0

    def agent(self, game):
        valid_moves = [col for col in range(game.columns) if game.board[0][col] == 0]
        action= -1
        while action == -1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    act = int(position[0] / game.cell_width)
                    if act in valid_moves:
                        action = act
        return action

    def replay(self, tie, game, player):
        pass

    def save(self):
        pass

    def load(self):
        pass

    def reset(self):
        self.win = 0
        self.lose = 0
        self.point = 0
        self.tie = 0
        self.match = 0

    def add_memory(self, state, action, reward):
        pass


class Random:
    def __init__(self, name='Random'):
        self.name = name
        self.win = 0
        self.lose = 0
        self.point = 0
        self.tie = 0
        self.match = 0

    def agent(self, game):
        valid_moves = [col for col in range(game.columns) if game.board[0][col] == 0]
        return random.choice(valid_moves)

    def replay(self, tie, game, player):
        pass

    def save(self):
        pass

    def load(self):
        pass

    def reset(self):
        self.win = 0
        self.lose = 0
        self.point = 0
        self.tie = 0
        self.match = 0

    def add_memory(self, state, action, reward):
        pass


class Reaction:
    def __init__(self, name='Reaction'):
        self.name = name
        self.win = 0
        self.lose = 0
        self.point = 0
        self.tie = 0
        self.match = 0

    def agent(self, game):
        valid_moves = [col for col in range(game.columns) if game.board[0][col] == 0]
        for i in valid_moves:
            board = game.drop_piece(game.board, i, game.current_player)
            win, _ = game.check_player_win(board,game.current_player)
            if win:
                return i
        player = [i+1 for i in range(game.n_players) if i+1 != game.current_player]
        for j in player:
            for i in valid_moves:
                board = game.drop_piece(game.board, i, j)
                win, _ = game.check_player_win(board,j)
                if win:
                    return i

        return random.choice(valid_moves)

    def replay(self, tie, game, player):
        pass

    def save(self):
        pass

    def load(self):
        pass

    def reset(self):
        self.win = 0
        self.lose = 0
        self.point = 0
        self.tie = 0
        self.match = 0

    def add_memory(self, state, action, reward):
        pass

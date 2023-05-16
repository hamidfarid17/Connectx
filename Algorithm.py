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
        action = -1
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
    """ Skill 1: Finds a move that leads to victory, otherwise it does a random move
        Skill 2: Finds a move that leads to victory,
                 otherwise finds a move that prevents the opponent from winning,
                 and otherwise makes a random move.
    """

    def __init__(self, name='Reaction', skill=None):
        if skill is None or 1 > skill > 2:
            self.skill = 2
        else:
            self.skill = skill
        self.name = name + '_' + str(self.skill)
        self.win = 0
        self.lose = 0
        self.point = 0
        self.tie = 0
        self.match = 0

    def agent(self, game):
        valid_moves = [col for col in range(game.columns) if game.board[0][col] == 0]
        for i in valid_moves:
            board = game.drop_piece(game.board, i, game.current_player)
            win, _ = game.check_player_win(board, game.current_player)
            if win:
                return i
        player = [i + 1 for i in range(game.n_players) if i + 1 != game.current_player]
        for j in player:
            for i in valid_moves:
                board = game.drop_piece(game.board, i, j)
                win, _ = game.check_player_win(board, j)
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


class MinMax:
    def __init__(self, name='MinMax', skill=None):
        if skill is None:
            self.skill = 5
        else:
            self.skill = skill
        self.name = name + '_' + str(self.skill)
        self.win = 0
        self.lose = 0
        self.point = 0
        self.tie = 0
        self.match = 0

    def agent(self, game):
        valid_moves = [col for col in range(game.columns) if game.board[0][col] == 0]
        _, mv = minmax(game, game.current_player, game.current_player, valid_moves,
                       0 if len(valid_moves) == game.columns else self.skill)
        return random.choice(mv)

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


def check_rew(board, r):
    for row in range(3):
        if board[row * 3 + 0] == board[row * 3 + 1] == board[row * 3 + 2] and board[row * 3] != 0:
            return r
    for col in range(3):
        if board[0 + col] == board[3 + col] == board[6 + col] and board[col] != 0:
            return r
    if board[0] == board[4] == board[8] and board[0] != 0:
        return r
    if board[2] == board[4] == board[6] and board[2] != 0:
        return r
    jj = [i for i in range(9) if board[i] == 0]
    if len(jj) == 0:
        return .5
    return 0


def minmax(game, my_turn, new_turn, action_list, deep):
    mm = []
    nt = []
    nn = []
    r = 1 if my_turn == new_turn else 2
    for i in action_list:
        b = game.drop_piece(game.board, i, new_turn)
        cr = game.check_player_win(b, r)
        if not cr and deep != 0:
            ac_list = [j for j in range(game.columns) if game.board[0][j] == 0]
            cr, _ = minmax(b, my_turn, 1 - new_turn, ac_list, deep - 1)
        mm.append(cr)
        nt.append(i)

    if my_turn == new_turn:
        mx = max(mm)
        for j in range(len(mm)):
            if mm[j] == mx:
                nn.append(nt[j])
        return mx, nn
    else:
        mx = min(mm)
        for j in range(len(mm)):
            if mm[j] == mx:
                nn.append(nt[j])
        return mx, nn

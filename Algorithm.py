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
    """ Skill 0: Finds a move that leads to victory, otherwise it does a random move
        Skill 1: Finds a move that leads to victory,
                 otherwise finds a move that prevents the opponent from winning,
                 and otherwise makes a random move.
    """

    def __init__(self, name='Reaction', skill=None):
        if skill is None:
            self.skill = 1
        elif skill < 0:
            self.skill = 0
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
        if self.skill > 0:
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
        _, mv = minmax(game, game.board, game.current_player, game.current_player, valid_moves, self.skill)
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


def minmax(game, board, my_turn, new_turn, action_list, deep):
    r = 1 if my_turn == new_turn else -1
    if len(action_list)==0:
        return 0, None
    cr, mv = check_reward(game, board, action_list, new_turn, r)
    if cr==0 and deep!=0:
        mm = []
        for col in mv:
            b = game.drop_piece(board, col, new_turn)
            valid_moves = [col for col in range(game.columns) if b[0][col] == 0]
            cr, _ = minmax(game, b, my_turn, 3-new_turn, valid_moves, deep-1)
            mm.append(cr)
        cr= max(mm)
        mv= [mv[j] for j in range(len(mm)) if mm[j] == max(mm)]

    return cr*r, mv


def check_reward(game, board, action_list, turn, r):
    cr = []
    for col in action_list:
        b = game.drop_piece(board, col, turn)
        cp, _ = game.check_player_win(b, turn)
        cr.append(cp * 1)
    # print(board)
    # print('cr=',cr)
    # print('al=',action_list)
    mx = max(cr)
    if mx == 0:
        cr = []
        turn = 3 - turn
        for col in action_list:
            b = game.drop_piece(board, col, turn)
            cp, _ = game.check_player_win(b, turn)
            cr.append(cp * 1)
            mx = max(cr) * -1

    return mx, [action_list[j] for j in range(len(cr)) if cr[j] == max(cr)]

#     for i in valid_moves:
#         board = game.drop_piece(game.board, i, j)
#         win, _ = game.check_player_win(board, j)
#         if win:
#             return i
#
# return random.choice(valid_moves)

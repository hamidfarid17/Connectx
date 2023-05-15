import time
from operator import attrgetter

import numpy as np
import pygame
from pygame.time import delay

from Constant import *


class Connectx:
    def __init__(self, players, width=720, height=480, columns=7, rows=6, in_rows=4, n_players=2, dly=100, ui=True):
        self.ui = ui
        self.players = players
        self.dly = dly
        self.width = width
        self.height = height
        self.n_players = n_players
        self.in_rows = in_rows
        self.rows = rows
        self.columns = columns
        self.board = np.zeros((rows, columns), dtype=int)
        self.current_player = 1
        self.game_over = False
        self.winner = 0
        self.cell_height = height / rows
        self.cell_width = width / columns
        self.radius = min(self.cell_width, self.cell_height) / 3
        if ui:
            pygame.init()
            self.screen = pygame.display.set_mode((width, height))
            pygame.font.init()
            color = COLORS[0]
            for i in range(self.rows):
                for j in range(self.columns):
                    x = j * self.cell_width + self.cell_width / 2
                    y = i * self.cell_height + self.cell_height / 2
                    pygame.draw.circle(self.screen, color, (x, y), self.radius)
            pygame.display.flip()

    def play_game(self):
        cap = ''
        for player in self.players:
            cap += '{}:{}, {}, {} - '.format(player.name, player.win, player.lose, player.tie)
        pygame.display.set_caption(cap[:-3])
        while not self.game_over:
            action = self.players[self.current_player - 1].agent(self)
            state = self.board.copy()
            self.update(action)
            self.check_connect()
            self.players[self.current_player - 1].add_memory(state, action, 0 if self.winner <= 0 else 1)
            self.next_player()
        for i, player in enumerate(self.players):
            player.match += 1
            if self.winner == 0:
                player.tie += 1
                player.point += .5
            elif i + 1 == self.winner:
                player.win += 1
                player.point += 1.
            elif self.winner > 0:
                player.lose += 1
            elif i + 1 == -self.winner:
                player.lose += 1
            else:
                player.win += 1
                player.point += 1.

        return self.winner

    def update(self, move):
        b = self.board[:, move]
        for i in range(self.rows - 1, -1, -1):
            if b[i] == 0:
                b[i] = self.current_player
                if self.ui:
                    if self.dly > 0:
                        for j in range(i):
                            color = COLORS[self.current_player]
                            x = move * self.cell_width + self.cell_width / 2
                            y = j * self.cell_height + self.cell_height / 2
                            pygame.draw.circle(self.screen, color, (x, y), self.radius)
                            pygame.display.flip()
                            delay(self.dly)
                            color = COLORS[0]
                            x = move * self.cell_width + self.cell_width / 2
                            y = j * self.cell_height + self.cell_height / 2
                            pygame.draw.circle(self.screen, color, (x, y), self.radius)

                    color = COLORS[self.current_player]
                    x = move * self.cell_width + self.cell_width / 2
                    y = i * self.cell_height + self.cell_height / 2
                    pygame.draw.circle(self.screen, color, (x, y), self.radius)
                    pygame.display.flip()
                return
        self.game_over = True
        self.winner = -self.current_player

    def draw_line(self, i1, j1, i2, j2, color):
        x1 = j1 * self.cell_width + self.cell_width / 2
        y1 = i1 * self.cell_height + self.cell_height / 2
        x2 = j2 * self.cell_width + self.cell_width / 2
        y2 = i2 * self.cell_height + self.cell_height / 2
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), width=10)
        pygame.display.flip()

    def next_player(self):
        self.current_player = self.current_player % self.n_players + 1

    def check_connect(self):
        win, line = self.check_player_win(self.board, self.current_player)
        if win:
            self.game_over = True
            self.winner = self.current_player
            if self.ui:
                x1, y1, x2, y2, color = line
                self.draw_line(x1, y1, x2, y2, color)
            delay(self.dly * 50)
        elif 0 not in self.board:
            self.game_over = True
            self.winner = 0
            delay(self.dly * 50)

    def drop_piece(self, board, col, piece):
        board = board.copy()
        for row in range(self.rows - 1, -1, -1):
            if board[row][col] == 0:
                break
        board[row][col] = piece
        return board

    def check_player_win(self, board, player):

        # horizontal
        for i in range(self.rows):
            for j in range(self.columns - self.in_rows + 1):
                if np.all(board[i, j:j + self.in_rows] == player):
                    return True, (i, j, i, j + self.in_rows - 1, COLORS[player])

        # vertical
        for i in range(self.rows - self.in_rows + 1):
            for j in range(self.columns):
                if np.all(board[i:i + self.in_rows, j] == player):
                    return True, (i, j, i + self.in_rows - 1, j, COLORS[player])

        # diagonal
        for i in range(self.rows - self.in_rows + 1):
            for j in range(self.columns - self.in_rows + 1):
                el = board[i][j]
                flag = True
                for c in range(self.in_rows):
                    if el != board[i + c][j + c] or board[i + c][j + c] != player:
                        flag = False
                if flag:
                    return True, (i, j, i + self.in_rows - 1, j + self.in_rows - 1, COLORS[player])

        for i in range(self.in_rows - 1, self.rows):
            for j in range(self.columns - self.in_rows + 1):
                el = board[i][j]
                flag = True
                for c in range(self.in_rows):
                    if el != board[i - c][j + c] or board[i - c][j + c] != player:
                        flag = False
                if flag:
                    return True, (i, j, i - self.in_rows + 1, j + self.in_rows - 1, COLORS[player])

        return False, None


def play_n_game(players, p1, p2, num, num_s, N, dly, ui):
    pl = [0, 0, 0]
    tm = time.time()
    if N > 100:
        n = N // 100
    else:
        n = 1
    for i in range(N):
        player = [players[p1], players[p2]]
        game = Connectx(player, n_players=2, dly=dly, ui=ui)
        game.play_game()

        players[p1].replay(game.winner == 0, game, 1)
        players[p2].replay(game.winner == 0, game, 2)

        if game.winner == 1:
            pl[0] += 1
        elif game.winner == 2:
            pl[1] += 1
        else:
            pl[2] += 1

        if i % n == n - 1:
            t2 = time.time()
            print('\r{:2}/{:2}-p{:3.0%} time:{:13}'.
                  format(num + 1, num_s, (i + 1) / N, change_time(t2 - tm)), end='  ***  ')
            print('{:10}:{:4.2%}, {:10}:{:4.2%}, Tie:{:4.2%}'.
                  format(players[p1].name, (pl[0]) / (i + 1), players[p2].name, (pl[1]) / (i + 1),
                         (pl[2]) / (i + 1)), end='')

    print('\r{:2}/{:2}-full time:{:13}  ***  {:20}:{:4.2%}, {:20}:{:4.2%}, Tie:{:4.2%}'.
          format(num + 1, num_s, change_time(time.time() - tm),
                 players[p1].name, pl[0] / N, players[p2].name, pl[1] / N, pl[2] / N))


def play(player, num, N, sweep=True, rst=True, league=True, dly=0, ui=True):
    nn = num
    MP_list = MP_League_export(len(player), sweep) if league else MP_Friendly_export(len(player), sweep)

    while num > 0:
        num -= 1
        for n, (i, j) in enumerate(MP_list):
            play_n_game(player, i, j, n, len(MP_list), N, dly, ui)
        dd = 'Game {:d}'.format(nn - num)
        print('////////////////////////////////////////{:^15}////////////////////////////////////////'.format(dd))
        new_team = sorted(player, key=attrgetter('point', 'win', 'tie'), reverse=True)

        for i in new_team:
            print('/////{:20} match:{:6}  point:{:1.2f}  win:{:6d}  lose:{:6d}  Tie:{:6d}   /////'.
                  format(i.name, i.match,
                         i.point / i.match,
                         i.win,
                         i.lose,
                         i.tie))
        print('///////////////////////////////////////////////////////////////////////////////////////////////')
        for i in player:
            i.save()
            if rst:
                i.reset()

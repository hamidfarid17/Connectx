import pickle
from collections import deque

import numpy as np
from torch import nn
from Constant import *


class QTable:
    def __init__(self, name='policy'):
        self.name = name
        self.policy = {}
        self.my_lr = .5
        self.max = 1.0
        self.epsilon = 1.0
        self.load()
        self.win = 0
        self.lose = 0
        self.point = 0
        self.tie = 0
        self.match = 0
        self.buffer = deque()

    def save(self):
        mx = self.lose / self.match
        if self.max != 0 or mx != 0:
            self.max = mx
            with open('Checkpoint/' + self.name + '.ql', 'wb') as f:
                pickle.dump([self.policy, self.my_lr, self.max, self.epsilon], f)
            print('++++++++++++++++  Save {}.ql  = {}  , lose={:.2%}  , epsilon={:,}'.
                  format(self.name, len(self.policy), self.max, self.epsilon))

    def load(self):
        try:
            with open('Checkpoint/' + self.name + '.ql', 'rb') as f:
                self.policy, self.my_lr, self.max, self.epsilon = pickle.load(f)
            print('++++++++++++++++  Load {}.ql  = {}  , lose={:.2%}  , epsilon={:,}'.
                  format(self.name, len(self.policy), self.max, self.epsilon))
        except:
            print('!!!!!!!!!!!!!!!! {}.ql not load'.format(self.name))

    def agent(self, game):
        valid_moves = [col for col in range(game.columns) if game.board[0][col] == 0]
        if random.random() < self.epsilon and RANDOM:
            action = int(random.choice(valid_moves))
        else:
            mv = []
            for jj in valid_moves:
                b = game.board.copy()
                _, r = self.get_value(b, jj, game, game.current_player)
                mv.append(r)
            action = valid_moves[np.random.choice(np.where(mv == np.amax(mv))[0])]
        return action

    def replay(self, tie, game, player):
        if self.max > 0:
            new_state, action, reward = self.buffer.pop()
            if tie:
                reward = .2
            new_sts, new_st_value = self.get_value(new_state, action, game, player)
            self.policy[new_sts] = (1 - self.my_lr) * new_st_value + self.my_lr * float(reward)

            while len(self.buffer) > 0:
                state, action, reward = self.buffer.pop()
                valid_moves = [col for col in range(game.columns) if state[0][col] == 0]
                mv = []
                for jj in valid_moves:
                    b = new_state.copy()
                    _, r = self.get_value(b, jj, game, player)
                    mv.append(r)
                if len(mv) == 0:
                    print(mv)
                rew = np.amax(mv)

                new_sts, st_value = self.get_value(state, action, game, player)

                self.policy[new_sts] = st_value * (1 - self.my_lr) + self.my_lr * rew
                new_state = state.copy()
            if RANDOM:
                if self.epsilon > 0.0:
                    self.epsilon -= 1e-5
                else:
                    self.epsilon = 0.0

            if self.my_lr <= .1:
                self.my_lr = 1e-5
            else:
                self.my_lr *= 1 - 1e-6
        else:
            self.buffer.clear()

    def reset(self):
        self.win = 0
        self.lose = 0
        self.point = 0
        self.tie = 0
        self.match = 0

    def add_memory(self, state, action, reward):
        self.buffer.append((state, action, reward))

    def get_value(self, state, action, game, player):
        new_board = game.drop_piece(state, action, player).flatten()
        s = new_board.tobytes()
        r = self.policy[s] if s in self.policy.keys() else 0
        return s, r


class QNeural:
    def __init__(self, layers=None):
        self.my_lr = LR
        self.max = 1.0
        self.number_of_games = 0
        self.epsilon = 1.0
        if layers is None:
            layers = [168, 28]
        name = ''
        for i in layers:
            name += str(i) + '_'
        self.name = 'AI_' + name[:-1]
        self.net = DQN(layers, 42, 7)
        self.load()
        self.win = 0
        self.lose = 0
        self.point = 0
        self.tie = 0
        self.match = 0
        self.optimizer = torch.optim.SGD(self.net.parameters(), lr=self.my_lr)
        self.loss_function = nn.MSELoss()
        self.buffer = deque()

    def agent(self, game):
        if random.random() < self.epsilon and RANDOM:
            valid_moves = [col for col in range(game.columns) if game.board[0][col] == 0]
            action = int(random.choice(valid_moves))
        else:
            state = torch.tensor(np.array([game.board.flatten()]), dtype=torch.float).to(device)
            action_probs = self.net.forward(state)
            _, action = torch.max(action_probs, dim=1)
            action = int(action.item())
        return action

    def replay(self, tie, game, player):
        if self.max > 0:
            self.number_of_games += 1
            state, action, reward = self.buffer.pop()
            if tie:
                reward = .8
            state_v = torch.tensor(np.array([state.flatten()]), dtype=torch.float).to(device)
            output = self.net.forward(state_v)
            target = output.clone().detach()
            illegal_list = [col for col in range(game.columns) if state[0][col] != 0]
            for i in illegal_list:
                target[0][i] = 0.0
            target[0][action] = float(reward)
            new_state = state.copy()
            loss = self.loss_function(output, target)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            while len(self.buffer) > 0:
                state, action, reward = self.buffer.pop()
                state_v = torch.tensor(np.array([new_state.flatten()]), dtype=torch.float).to(device)
                next_q_values = self.net.forward(state_v)
                rew = torch.max(next_q_values).item()

                state_v = torch.tensor(np.array([state.flatten()]), dtype=torch.float).to(device)
                output = self.net.forward(state_v)
                target = output.clone().detach()
                illegal_list = [col for col in range(game.columns) if state[0][col] != 0]
                for i in illegal_list:
                    target[0][i] = 0.
                target[0][action] = rew * AI_GAMMA
                new_state = state

                loss = self.loss_function(output, target)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
            if RANDOM:
                if self.epsilon > 0.0:
                    self.epsilon -= 5e-7
                else:
                    self.epsilon = 0.0
        else:
            self.buffer.clear()

    def save(self):
        mx = self.lose / self.match
        if self.max != 0 or mx != 0:
            self.max = mx
            torch.save({
                'model_state_dict': self.net.state_dict(),
                'lr': self.my_lr,
                'epsilon': self.epsilon,
                'game': self.number_of_games,
                'max': self.max}, 'Checkpoint/' + self.name + '.ai')
            print('++++++++++++++++  Save {}.ai  =  {} , lose={:.2%} , epsilon ={}, number of Games: {:,}'.
                  format(self.name, self.my_lr, self.max, self.epsilon,self.number_of_games))

    def load(self):
        try:
            checkpoint = torch.load('Checkpoint/' + self.name + '.ai')
            self.net.load_state_dict(checkpoint['model_state_dict'])
            self.my_lr = checkpoint['lr']
            self.epsilon = checkpoint['epsilon']
            self.number_of_games = checkpoint['game']
            self.max = checkpoint['max']
            print('load {}.ai  =  {} , lose={:.2%} , epsilon ={}, number of Games: {:,}'.
                  format(self.name, self.my_lr, self.max, self.epsilon,self.number_of_games))
        except:
            print('{}.ai not load'.format(self.name))

    def reset(self):
        self.win = 0
        self.lose = 0
        self.point = 0
        self.tie = 0
        self.match = 0

    def add_memory(self, state, action, reward):
        self.buffer.append((state, action, reward))


class DQN(nn.Module):
    def __init__(self, layer, n_in, n_out):
        super(DQN, self).__init__()
        layers = []
        for l in layer:
            layers.append(nn.Linear(n_in, l))
            layers.append(nn.ReLU())
            n_in = l
        layers.append(nn.Linear(n_in, n_out))
        layers.append(nn.Sigmoid())
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)

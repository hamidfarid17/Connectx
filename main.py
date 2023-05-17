import os
import time

import Algorithm, AI
import Connectx
from Constant import change_time

if __name__ == "__main__":
    path = './Checkpoint'
    # check whether directory already exists
    if not os.path.exists(path):
        os.mkdir(path)

    players = []
    # players.append(AI.QNeural([96, 96, 96, 96, 96, 28]))
    # players.append(AI.QNeural([256,256,256,256,256]))
    # players.append(AI.QNeural([256,256,28]))
    # players.append(AI.QTable())
    # players.append(AI.QTable())
    players.append(Algorithm.Reaction('Reaction_A',skill=1))
    # players.append(Algorithm.Reaction('Reaction_B',skill=1))
    players.append(Algorithm.Random())
    # players.append(Algorithm.MinMax(name='MINMAX_A', skill=5))
    # players.append(Algorithm.MinMax(skill=2))
    # players.append(Algorithm.Human())
    # players.append(Algorithm.MinMax(1))
    # players.append(Algorithm.MinMax(2))
    # players.append(Algorithm.MinMax(3))
    # players.append(Algorithm.MinMax(4))
    # players.append(Algorithm.MinMax(5))

    t = time.time()
    Connectx.play(players, 5000, 1000, sweep=True, rst=True, league=False, ui=False, dly=0)
    print('time= {}'.format(change_time(time.time() - t)))

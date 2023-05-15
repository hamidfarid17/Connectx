import os
import time


import Algorithm, AI
import Connectx

if __name__ == "__main__":
    path = './Checkpoint'
    # check whether directory already exists
    if not os.path.exists(path):
        os.mkdir(path)

    players = []
    players.append(AI.QNeural([256,256,28]))
    # players.append(AI.QTable())
    # players.append(AI.QTable())
    # players.append(Algorithm.Reaction('R1'))
    # players.append(Algorithm.Reaction('R2'))
    players.append(Algorithm.Random())
    # players.append(Algorithm.Random())
    # players.append(Algorithm.Human())
    # players.append(Algorithm.MinMax(1))
    # players.append(Algorithm.MinMax(2))
    # players.append(Algorithm.MinMax(3))
    # players.append(Algorithm.MinMax(4))
    # players.append(Algorithm.MinMax(5))

    t = time.time()
    Connectx.play(players, 50, 100000, sweep=True, rst=True, league=True, ui=False)
    print(time.time() - t)

    players = []
    players.append(AI.QNeural())
    players.append(Algorithm.Reaction())

    t = time.time()
    Connectx.play(players, 5000, 1000, sweep=True, rst=False, league=True, ui=False)
    print(time.time() - t)

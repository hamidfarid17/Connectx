import os
import random

import torch

COLORS = [(255, 255, 255),
          (255, 0, 0),
          (0, 255, 0),
          (0, 0, 255),
          (128, 0, 255)]

LR = .1
device = torch.device("cpu")
AI_GAMMA = .99
RANDOM = True

os.environ['SDL_VIDEO_WINDOW_POS'] = "1200,200"

def MP_League_export(number, sweep=True):
    l = list(range(0, number))
    week = number - 1 if number % 2 == 0 else number
    MP = []
    i = 0
    while i < week:
        m = l.copy()
        cash = []
        loop_test = 0
        while len(m) > 1:
            a, b = random.choices(m, k=2)

            if a != b:
                if (a, b) not in MP and (b, a) not in MP:
                    cash.append((a, b))
                    m.remove(a)
                    m.remove(b)
                elif len(m) < 4:
                    loop_test += 1
                    if loop_test == 20 or len(l) < 4:
                        MP.clear()
                        cash.clear()
                        i = -1

                        break
                    else:
                        a, b = cash.pop()
                        m.append(a)
                        m.append(b)

        MP += cash
        i += 1
    if sweep:
        cash = []
        for a, b in MP:
            cash.append((b, a))
            # cash.append((a, b))
        MP += cash
    return MP


def MP_Friendly_export(number, sweep=True):
    l = list(range(1, number))
    mp = []
    for i in range(number - 1):
        mp.append((0, l[i]))

    if sweep:
        cash = []
        for a, b in mp:
            cash.append((b, a))
        mp += cash
    return mp


def change_time(t):
    s = ''
    tt = t
    if tt > 3600:
        m = t // 3600
        s = '{:02d}:'.format(int(m))
        tt -= m * 3600
    if tt > 60:
        m = tt // 60
        s += '{:02d}:'.format(int(m))
        tt -= m * 60
    s += '{:02d}'.format(int(tt))
    return s

############################
### Day 1
############################

### Day 1.1
res = []
with open('data/input1.txt') as f:
    res_k = 0
    for line in f:
        row = line.strip()
        if row == "":
            res.append(res_k)
            res_k = 0
        else:
            res_k += int(row)
max(res)

### Day 1.2
res.sort(reverse=True)
sum(res[0:3])


############################
### Day 2
############################
import numpy as np
import pandas as pd

dt = pd.read_csv('data/input2.txt', header=None, sep=" ", names=["ADV", "ME"])

def get_score(row):
    me = row["ME"]
    adv = row["ADV"]
    if me == "X":
        score = 1
        if adv == "A": #draw
            score += 3
        elif adv == "B": #lost
            score += 0
        elif adv == "C": #win
            score += 6
    elif me == "Y":
        score = 2
        if adv == "A": #win
            score += 6
        elif adv == "B": #draw
            score += 3
        elif adv == "C": #lost
            score += 0
    elif me == "Z":
        score = 3
        if adv == "A": #lost
            score += 0
        elif adv == "B": #win
            score += 6
        elif adv == "C": #draw
            score += 3
    return(score)

res_1_1 = np.sum(dt.apply(lambda x: get_score(x), axis = 1 ))
res_1_1

### Day 2.2
dt = dt.rename(columns={'ME': "RES"})
def get_shape(row):
    adv = row["ADV"]
    res = row["RES"]

    if res == "X": #lose
        if adv == "A": #rock
            me = 'Z'
        elif adv == "B": #paper
            me = 'X'
        elif adv == "C": #scissor
            me = 'Y'
    if res == "Y": #draw
        if adv == "A": #rock
            me = 'X'
        elif adv == "B": #paper
            me = 'Y'
        elif adv == "C": #scissor
            me = 'Z'
    if res == "Z": #win
        if adv == "A": #rock
            me = 'Y'
        elif adv == "B": #paper
            me = 'Z'
        elif adv == "C": #scissor
            me = 'X'
    return(me)

dt = dt.assign(ME = dt.apply(lambda x : get_shape(x), axis=1))
res_1_2 = np.sum(dt.apply(lambda x: get_score(x), axis = 1 ))
res_1_2
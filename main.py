import numpy as np
import pandas as pd


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

############################
### Day 3
############################
import string

### Day 3.1
dt = pd.read_csv('data/input3.txt', header=None, sep=" ", names=["pack"])

# Compute dictionnary for value of each letter
dic_low = dict(zip(string.ascii_lowercase, list(range(1, 27))))
dic_up = dict(zip(string.ascii_uppercase, list(range(27, 53))))
full_dict = dict(dic_low, **dic_up)

# Function to get value of item in common for a given pack

def get_common_value(row):
    len_row = len(row)
    pack1 = row[slice(0, len_row//2)]
    pack2 = row[slice(len_row//2, len_row)]
    common = list(set(pack1).intersection(set(pack2)))[0]
    value = full_dict[common]
    return value

res_3_1 = np.sum(dt.apply(lambda x: get_common_value(x['pack']), axis=1))
res_3_1

### Day 3.2
n = dt.shape[0]
n_group = n / 3

# Create column of group
L = [[i] * 3 for i in range(1, 101)]
groups = ["G"+ str(item) for sublist in L for item in sublist]
dt = dt.assign(groups=groups)

def get_common_value_group(dt_group):
    lst_set = [set(i) for i in dt_group['pack'].to_list()]
    common = list(set.intersection(*lst_set))[0]
    value = full_dict[common]
    return value


test = dt.iloc[0:3]
get_common_value_group(test)

# Apply on each group with groupby
dt_grouped = dt.groupby('groups').apply(get_common_value_group).reset_index(name="value")
res_3_2 = np.sum(dt_grouped['value'])
res_3_2
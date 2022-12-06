import numpy as np
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


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

############################
### Day 4
############################
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

### Day 4.1
dt = pd.read_csv('data/input4.txt', header=None, sep=",", names=["range1", "range2"])

# Transform input 2 ranges into two sets
def get_set_from_range(row):
    rang = row
    lst_int = [int(i) for i in rang.split("-")]
    set_int = set(list(range(lst_int[0], 1 + lst_int[1])))
    return set_int

dt = dt.assign(set1 = dt.apply(lambda x: get_set_from_range(x["range1"]), axis=1))
dt = dt.assign(set2 = dt.apply(lambda x: get_set_from_range(x["range2"]), axis=1))
dt.head()

# Return 1 if one set is contained into other
def is_recovered(row):
    tst1 = row["set1"].issubset(row["set2"])
    tst2 = row["set2"].issubset(row["set1"])
    res = 0
    if tst1 or tst2:
        res = 1
    return res

res_4_1 = np.sum(dt.apply(lambda x: is_recovered(x), axis=1))
res_4_1

### Day 4.2
def get_inter(row):
    tst1 = row["set1"].intersection(row["set2"])
    res = 0
    if len(tst1) > 0:
        res = 1
    return res


res_4_2 = np.sum(dt.apply(lambda x: get_inter(x), axis=1))
res_4_2

############################
### Day 5
############################

### Day 5.1
dt = pd.read_csv('data/input5.txt', header=None, sep=",",nrows=8,names=["V1"])
dt

# Try to convert stack in list of rows
need_el = [i for i in range(1, 34, 4)]
def get_list_rows(row):
    a1 = [*row["V1"]]
    a2 = [a1[i] for i in need_el]
    return a2


list_rows = dt.apply(lambda x: get_list_rows(x), axis=1)

# Create dictionnary of columns
dic_col = {}
for j in range(0, 9):
    col_j = list()
    for i in range(0, 8):
        col_j.append(list_rows.iloc[i][j])
    print(col_j)
    col_j.reverse()
    col_j_clean = [val for val in col_j if val != " "]
    col_dic_name = "col"+str(j+1)
    dic_col[col_dic_name] = col_j_clean
dic_col

# Read and apply all instructions
with open('data/input5.txt', "r") as f:
    for line in f.readlines():
        if line.startswith("move"):
            row = line
            row_lst = row.split()
            print(row_lst)
            nb_move = int(row_lst[1])
            col_1 = "col" + row_lst[3]
            col_2 = "col" + row_lst[5]
            for k in range(0, nb_move):
                val = dic_col[col_1].pop()
                dic_col[col_2].append(val)

# on recupere ensuite les derniers elements de chaque col de col_dict
res_5_1 = [dic_col[key][-1] for key in dic_col]
res_5_1 = ''.join(res_5_1)
res_5_1


### Day 5.2
# Create dictionnary of columns idem as part 1
dic_col = {}
for j in range(0, 9):
    col_j = list()
    for i in range(0, 8):
        col_j.append(list_rows.iloc[i][j])
    print(col_j)
    col_j.reverse()
    col_j_clean = [val for val in col_j if val != " "]
    col_dic_name = "col"+str(j+1)
    dic_col[col_dic_name] = col_j_clean
dic_col

# Read and apply all instructions
with open('data/input5.txt', "r") as f:
    for line in f.readlines():
        if line.startswith("move"):
            row = line
            row_lst = row.split()
            print(row_lst)
            nb_move = int(row_lst[1])
            col_1 = "col" + row_lst[3]
            col_2 = "col" + row_lst[5]
            temp = list()
            for k in range(0, nb_move):
                val = dic_col[col_1].pop()
                temp.append(val)
            temp.reverse()
            dic_col[col_2].extend(temp)

# on recupere ensuite les derniers elements de chaque col de col_dict
res_5_2 = [dic_col[key][-1] for key in dic_col]
res_5_2 = ''.join(res_5_1)
res_5_2

############################
### Day 6
############################


### Day 6.1

# Get data and transform in list of characters
with open('data/input6.txt', "r") as f:
    for line in f.readlines():
        dt = line
l_dt = [*dt]
n = len(l_dt)

# Window of size 4 compare len of list and len of set (wich is made of unique char)
for i in range(3, n):
    tmp = l_dt[(i-3):i+1]
    n_tmp = len(tmp)
    n_set = len(set(tmp))
    if n_set == n_tmp:
        print(tmp)
        print(i)
        print("Result = {0}".format(i+1))
        break

### Day 6.2
# Window of size 14 compare len of list and len of set (wich is made of unique char)
for i in range(13, n):
    tmp = l_dt[(i-13):i+1]
    n_tmp = len(tmp)
    n_set = len(set(tmp))
    if n_set == n_tmp:
        print(tmp)
        print(i)
        print("Result = {0}".format(i+1))
        break

############################
### Day 7
############################


### Day 7.1

############################
### Day 1
############################

### Day 1.1
res = []
with open('input1.txt') as f:
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


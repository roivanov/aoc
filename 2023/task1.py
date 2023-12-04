#!/bin/env python3

REPLACE = {'one':'1', 'two':'2', 'three':'3', 'four':'4', 'five':'5', 'six':'6', 'seven':'7', 'eight':'8', 'nine':'9'}
count=0
with open('data1') as f:
    for line in f.readlines():
        line = line.strip('\n')
        nums = []
        i = 0
        while i < len(line):
            if line[i].isdigit():
                nums.append(line[i])
            else:
                for k,v in REPLACE.items():
                    if line[i:].startswith(k):
                        nums.append(v)
                        break
            i+=1
        # print(line)
        # nums = [x for x in line if x.isdigit()]
        # print(nums)
        count += int(nums[0] + nums[-1])
        # break

assert count not in [53595,54194,]
print(count)

#!/bin/env python3

count=0
with open('data1') as f:
    for line in f.readlines():
        nums = [x for x in line if x.isdigit()]
        # print(nums)
        count += int(nums[0] + nums[-1])
        # break

print(count)

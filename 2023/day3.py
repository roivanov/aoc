#!/bin/env python3

RED='red'
GREEN='green'
BLUE='blue'
count=0
games_power=0

def process_line(arr_of_lines):
    ret = 0
    # print(arr_of_lines[1])
    # breakpoint()

    for i,j in spot_number(arr_of_lines[1]):
        # print(arr_of_lines[1][i:j])
        # print("L", arr_of_lines[1][i-1])
        # print("R", arr_of_lines[1][j])
        # print('TOP:', arr_of_lines[0][i-1:j+1])
        # print('DOWN', arr_of_lines[2][i-1:j+1])
        arr = arr_of_lines[1][i-1] + \
            arr_of_lines[1][j] + \
                arr_of_lines[0][i-1:j+1] + \
                    arr_of_lines[2][i-1:j+1]

        # print(arr)
        if any([x != '.' for x in arr ]):
            ret += int(arr_of_lines[1][i:j])

    return ret

def spot_number(s):
    i = 1
    while i < len(s):
        if s[i].isdigit():
            j=i+1
            while (j < len(s) and s[j].isdigit()):
                j+=1

            yield i,j
            i=j
        else:
            i+=1

def reader(name):
    arr = []
    with open(name) as f:
        for line in f.readlines():
            arr.append('.' + line.strip() + '.')
            if len(arr) == 2:
                yield ['.' * len(arr[0])] + arr
            elif len(arr) == 3:
                yield arr
                del arr[0]

        yield arr + ['.' * len(arr[0])]

if __name__ == '__main__':
    ret = 0
    for arr_of_lines in reader('day3-data2'):
        # print(arr_of_lines)
        ret += process_line(arr_of_lines)

print(ret)

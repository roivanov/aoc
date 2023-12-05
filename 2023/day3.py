#!/bin/env python3

class LineOfEngine:
    def __init__(self, s: str) -> None:
        self.s = s

    def len(self):
        return len(self.s)

    def __getitem__(self, indx):
        return self.s[indx]

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
    while i < s.len():
        if s[i].isdigit():
            j=i+1
            while (j < s.len() and s[j].isdigit()):
                j+=1

            yield i,j
            i=j
        else:
            i+=1

def reader(name):
    arr = []
    with open(name) as f:
        for line in f.readlines():
            arr.append(LineOfEngine('.' + line.strip() + '.'))
            if len(arr) == 2:
                yield [LineOfEngine('.' * arr[0].len())] + arr
            elif len(arr) == 3:
                yield arr
                del arr[0]

        yield arr + [LineOfEngine('.' * arr[0].len())]

if __name__ == '__main__':
    ret = 0
    for arr_of_lines in reader('day3-data2'):
        # print(arr_of_lines)
        ret += process_line(arr_of_lines)

    assert ret == 537732
    print(ret)

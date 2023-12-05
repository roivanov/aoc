#!/bin/env python3

class LineOfEngine:
    def __init__(self, s: str) -> None:
        self.s = s
        self.numbers = []

    def len(self):
        return len(self.s)

    def __getitem__(self, indx):
        return self.s[indx]

    def spot_number(self):
        i = 1
        while i < len(self.s):
            if self.s[i].isdigit():
                j=i+1
                while (j < len(self.s) and self.s[j].isdigit()):
                    j+=1

                self.numbers.append([i,j,int(self.s[i:j])])
                yield i,j
                i=j
            else:
                i+=1

    def number_at(self, i,j):
        for a,b,num in self.numbers:
            if a==i and b==j:
                return num

def process_line(arr_of_lines):
    ret = 0

    for i,j in arr_of_lines[1].spot_number():
        arr = arr_of_lines[1][i-1] + \
            arr_of_lines[1][j] + \
                arr_of_lines[0][i-1:j+1] + \
                    arr_of_lines[2][i-1:j+1]

        if any([x != '.' for x in arr ]):
            ret += arr_of_lines[1].number_at(i,j)

    return ret

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

    assert ret in [537732, 4361], ret
    print(ret)

from pathlib import Path

SAMPLE_DATA1 = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

class Sequence:
    def __init__(self, s) -> None:
        self.nums = [[int(x) for x in s.split()], ]
        while not all([x == 0 for x in self.nums[-1]]):
            self.nums.append([self.nums[-1][i] - self.nums[-1][i-1]
                              for i in range(1, len(self.nums[-1]))])
        # print(self.nums)

    def __repr__(self) -> str:
        return ', '.join(self.num)

    def next(self):
        self.nums[-1].append(0)
        for i in range(len(self.nums)-2, -1, -1):
            self.nums[i].append(self.nums[i][-1] + self.nums[i+1][-1])
        # print(self.nums)

    def last(self):
        return self.nums[0][-1]

    def first(self):
        first = 0
        for i in range(len(self.nums)-2, -1, -1):
            first = self.nums[i][0] - first
        return first

def test_seq_example1():
    arr = []
    for line in SAMPLE_DATA1.splitlines():
        if line:
            arr.append(Sequence(line.strip('\n')))

    for each in arr:
        each.next()

    assert len(arr) == 3
    assert sum([x.last() for x in arr]) == 114

    assert arr[-1].first() == 5

def test_seq_example1():
    arr = []
    with open(Path(__file__).parent / 'input.txt') as f:
        for line in f.readlines():
            if line:
                arr.append(Sequence(line.strip('\n')))

    for each in arr:
        each.next()

    assert len(arr) == 200
    assert sum([x.last() for x in arr]) == 2043183816
    assert sum([x.first() for x in arr]) == 1118

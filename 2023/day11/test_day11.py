from itertools import combinations
from pathlib import Path

SAMPLE_DATA1 = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

class TheMap:
    def __init__(self, s) -> None:
        self.map = list([x for x in self.expand_x(s)])
        self.expand_y()
        print(self)

    def expand_x(self, s):
        for each in [x for x in s.splitlines() if x]:
            yield each
            if set(each) == {'.'}:
                yield 'X' * len(each)

    def expand_y(self):
        for y in range(len(self.map[0]) -1, -1, -1):
            if all([self.map[x][y] in {'.', 'X'}
                    for x in range(0, len(self.map))]):
                for x in range(0, len(self.map)):
                    self.map[x] = self.map[x][:y] + 'X' + self.map[x][y:]

    def galaxy(self):
        for x in range(0, len(self.map)):
            for y in range(0, len(self.map[0])):
                if self.map[x][y] == '#':
                    yield x,y

    def dist(self, xpand=1):
        comb = combinations(self.galaxy(), 2)

        if xpand == 1:
            ret = sum([abs(a-x) + abs(b-y) for (a,b),(x,y) in comb])
        else:
            xpand -= 1
            ret = 0
            for (a,b),(x,y) in comb:
                ret += sum([xpand if self.map[i][y] == 'X' else 1
                            for i in range(a,x, 1 if a<x else -1)])
                ret += sum([xpand if self.map[a][j] == 'X' else 1
                            for j in range(b,y, 1 if b<y else -1)])

        return ret

    def __str__(self) -> str:
        return '\n'.join(self.map)

def test_seq_example1():
    m = TheMap(SAMPLE_DATA1)

    assert len(m.map) == 12
    assert len(m.map[0]) == 13

    gal = list(m.galaxy())
    assert len(gal) == 9

    comb = list(combinations(gal, 2))
    assert len(comb) == 36

    dist = sum([abs(a-x) + abs(b-y) for (a,b),(x,y) in comb])
    assert dist == 374
    assert m.dist() == 374
    assert m.dist(10) == 1030
    assert m.dist(100) == 8410

def test_input():
    m = TheMap((Path(__file__).parent / 'input.txt').read_text())
    assert len(m.map) == 146
    assert m.dist() == 10033566
    assert m.dist(1000000) == 560822911938

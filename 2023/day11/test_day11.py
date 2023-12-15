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
        self.map = []
        for each in [x for x in s.splitlines() if x]:
            self.map.append(each)
            if set(each) == {'.'}:
                self.map.append(each)

        for y in range(len(self.map[0]) -1, -1, -1):
            if all([self.map[x][y] == '.'
                    for x in range(0, len(self.map))]):
                for x in range(0, len(self.map)):
                    self.map[x] = self.map[x][:y] + '.' + self.map[x][y:]

    def galaxy(self):
        for x in range(0, len(self.map)):
            for y in range(0, len(self.map[0])):
                if self.map[x][y] == '#':
                    yield x,y


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
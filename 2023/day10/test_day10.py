from pathlib import Path

SAMPLE1 = """
.....
.S-7.
.|.|.
.L-J.
.....
"""

SAMPLE2 = """
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""

SAMPLE3 = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

SAMPLE4 = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

class Coord:
    def __init__(self,x,y) -> None:
        self.x=x
        self.y=y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

class Vector(Coord):
    def __repr__(self) -> str:
        return f"V:{self}"

    def reversed(self):
        return Vector(-self.x, -self.y)

class Point(Coord):
    def __add__(self, other:Vector):
        return Point(self.x + other.x, self.y + other.y)

VECTORS = {
    '|': [(Vector(1,0), Vector(1,0)),],
    '-': [(Vector(0,1), Vector(0,1)),],
    '7': [(Vector(0,1), Vector(1,0)),],
    'L': [(Vector(1,0), Vector(0,1)),],
    'F': [(Vector(-1,0), Vector(0,1)),],
    'J': [(Vector(0,1), Vector(-1,0)),],
}

for v in VECTORS.values():
    v.append((v[0][1].reversed(), v[0][0].reversed()))

ALL_DIRECTIONS = [v for v in [Vector(x,y)
                              for x in [-1,0,1]
                              for y in [-1,0,1]]
                              if v != Vector(0,0)]

class PipePath:
    def __init__(self, lines) -> None:
        self.map = []
        for line in lines:
            if line:
                self.map.append([x for x in line.strip()])

        print(self.map)

    @property
    def start(self):
        for indx, row in enumerate(self.map):
            if 'S' in row:
                return Point(indx, row.index('S'))
        return None

    def get_at(self, p):
        if p.x >=0 and p.y >= 0:
            return self.map[p.x][p.y]
        else:
            return None

    def iter_moves(self, start, direct):
        for v in direct:
            val = self.get_at(start + v)
            if val in ['.', None]:
                continue
            if val in VECTORS:
                for first, second in VECTORS[val]:
                    if v == first:
                        yield first, second
            else:
                raise IndexError(f"bad {val}")

    def next(self, start, direct):
        print(start, direct)
        moves = list(self.iter_moves(start, direct))

        assert len(moves) == 2 if len(direct) == 8 else 1

        for each in moves:
            yield each

    @property
    def farthest(self):
        start = self.start
        (v11, v12), (v21, v22) = self.next(self.start, ALL_DIRECTIONS)
        print((v11, v12), (v21, v22))
        next_step = start + v11
        last_step = start + v22
        count = 2

        # do we need to compare directions here?
        while next_step != last_step:
            count+=1
            ret = list(self.next(next_step, [v12,]))
            assert len(ret) == 1
            v11, v12 = ret[0]
            next_step += v11

        return count // 2

def test_seq_example1():
    pp1 = PipePath(SAMPLE1.splitlines())

    # with open(Path(__file__).parent / 'input.txt') as f:
    #     pass

    assert pp1.start == Point(1,1)
    assert pp1.farthest == 4

def test_seq_example2():
    pp1 = PipePath(SAMPLE2.splitlines())

    assert pp1.start == Point(1,1)
    assert pp1.farthest == 4

def test_seq_example3():
    pp1 = PipePath(SAMPLE3.splitlines())

    assert pp1.start == Point(2,0)
    assert pp1.farthest == 8

def test_seq_example4():
    pp1 = PipePath(SAMPLE4.splitlines())

    assert pp1.start == Point(2,0)
    assert pp1.farthest == 8

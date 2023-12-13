from collections import deque
from math import atan2, pi
from pathlib import Path

from input import SAMPLE21

import pytest

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

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    def __radd__(self, other):
        return other + self.x

class Vector(Coord):
    def __repr__(self) -> str:
        return f"V:{self}"

    def reversed(self):
        return Vector(-self.x, -self.y)

    @property
    def angle(self):
        return 180 * atan2(self.y, self.x)/pi

class Point(Coord):
    pass

def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


class Line:
    def __init__(self, a:Point, b:Point) -> None:
        self.a = a
        self.b = b

    def intersect(self, other):
        ret = intersect(self.a, self.b, other.a, other.b)
        touches = any([x == y for x in [self.a, self.b] for y in [other.a, other.b]])
        return ret and not touches

    def count_intersect(self, others):
        return sum([self.intersect(x) == True for x in others])

    def __str__(self) -> str:
        return f"{self.a}->{self.b}"

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

    def __str__(self) -> str:
        return '\n'.join([''.join(x) for x in self.map])

    def len(self):
        return len(self.map)

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

    def next(self, start, direct):
        for v in direct:
            val = self.get_at(start + v)
            if val in ['.', None]:
                continue

            for first, second in VECTORS[val]:
                if v == first:
                    yield first, second

    @property
    def farthest(self):
        start = self.start
        (v11, v12), (v21, v22) = self.next(start, ALL_DIRECTIONS)
        next_step = start + v11
        last_step = start + v21
        count = 2

        # do we need to compare directions here?
        while next_step != last_step:
            count+=1
            ret = list(self.next(next_step, [v12,]))
            assert len(ret) == 1
            v11, v12 = ret[0]
            next_step += v11

        return count // 2

    def each_point(self):
        for row, _ in enumerate(self.map):
            for col, _ in enumerate(self.map[row]):
                yield Point(row, col)

    def set_at(self, p, value):
        self.map[p.x][p.y] = value

    def neighbors(self, p: Point):
        """Find all neightbors of the point p which are dots '.'
        """
        visited = []
        yet_to_check = deque([p,])

        for each in yet_to_check:
            for dir in ALL_DIRECTIONS:
                coord = each + dir
                p1 = Point(coord.x, coord.y)
                # print(p1.x, p1.y)
                assert isinstance(p1, Point)
                if p1 not in visited:
                    val = self.get_at(p1)
                    if val == '.':
                        visited.append(p1)
                        yield p1

    @property
    def straight(self):
        start = self.start
        turn_points = [start]

        (v11, v12), (v21, _) = self.next(start, ALL_DIRECTIONS)
        next_step = start + v11
        last_step = start + v21

        while next_step != last_step:
            if self.get_at(next_step).isalnum():
                turn_points.append(next_step)
            v11, v12 = list(self.next(next_step, [v12,]))[0]
            next_step += v11

        assert len(turn_points) == 12
        turn_points.append(start)
        lines = []
        for i in range(len(turn_points)-1):
            lines.append(Line(turn_points[i], turn_points[i+1]))

        assert len(lines) == 12
        print(self)

        for p in self.each_point():
            if self.get_at(p) == '.':
                tline = Line(start, p)
                crosses = tline.count_intersect(lines)
                if crosses > 0 and crosses % 2 == 0:
                    self.set_at(p, str(crosses))
                    for n in self.neighbors(p):
                        self.set_at(n, str(crosses))

        print(self)

        def isdigit_but7(x):
            return x != '7' and x.isdigit()

        return sum([1 if isdigit_but7(self.get_at(x)) else 0
                    for x in self.each_point()])

def test_seq_example1():
    pp1 = PipePath(SAMPLE1.splitlines())

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

def test_seq_test1():
    for v in VECTORS.values():
        assert len(v) == 2
        assert sum([sum(y) for y in v]) == 0

    with open(Path(__file__).parent / 'input.txt') as f:
        pp1 = PipePath(f.readlines())

    start = pp1.start
    (v11, _), (v21, _) = pp1.next(start, ALL_DIRECTIONS)
    next_step = start + v11
    last_step = start + v21
    assert {pp1.get_at(next_step), pp1.get_at(last_step)} == {'|', 'L'}

    assert pp1.len() == 140
    assert pp1.start == Point(25,108), f"{pp1.start}"
    assert pp1.get_at(Point(25,108)) == 'S'
    assert pp1.farthest == 6701

def test_seq_test21():
    assert Line(Point(0,0), Point(10,0)).intersect(
            Line(Point(5,1), Point(5,-1))) == True
    assert Line(Point(0,0), Point(10,0)).intersect(
            Line(Point(5,-10), Point(5,-1))) == False

    pp1 = PipePath(SAMPLE21.splitlines())
    assert pp1.len() == 9
    start = pp1.start
    assert start == Point(1,1), f"{start}"
    assert pp1.get_at(Point(1,1)) == 'S'

    (v11, _), (v21, _) = pp1.next(start, ALL_DIRECTIONS)
    next_step = start + v11
    last_step = start + v21
    assert {pp1.get_at(next_step), pp1.get_at(last_step)} == {'|', '-'}

    assert pp1.farthest == 23

    assert pp1.straight == 4

def test_so6():
    """
    https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
    """
    A=Point(0,0)
    B=Point(10,0)
    C=Point(5,-1)
    D=Point(5,-10)
    assert intersect(A,B,C,D) == False

def test_so7():
    A=Point(0,0)
    B=Point(10,0)
    C=Point(5,10)
    D=Point(5,-10)
    assert intersect(A,B,C,D) == True

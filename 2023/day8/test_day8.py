from itertools import cycle
import math
import re

SAMPLE_DATA1="""
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

SAMPLE_DATA2="""
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

pattern = re.compile(r'(\S+) = \((\S+), (\S+)\)')

class Node:
    AllNodes = {}
    def __init__(self, s) -> None:
        m = pattern.match(s)
        # print(m.groups())
        self.name, self.left, self.right = m.groups()
        # self.l = Node.AllNodes.get(self.left, None)
        # self.r = Node.AllNodes.get(self.right, None)
        self.l = None
        self.r = None
        Node.AllNodes[self.name] = self

        if self.name.endswith('A'):
            self.ends = [self]
            self.steps = [0]

        self.__next = None

    def next(self, s):
        if self.__next is None:
            self.__next = {'L': self.l, 'R': self.r}
        return self.__next[s]

    def __repr__(self) -> str:
        if self.name.endswith('A'):
            return f"Node: {self.name} -> {self.steps[-1]} {self.ends[-1].name}"
        else:
            return f"Node: {self.name}"


def test_pattern():
    n = Node('AAA = (BBB, CCC)')

    assert n.name == 'AAA'
    assert n.left == 'BBB'
    assert n.right == 'CCC'

def test_demo1():
    lines = SAMPLE_DATA1.splitlines()
    path = lines[1]
    assert path == 'RL'

    nodes = {x.name: x for x in [Node(x) for x in lines[3:]]}
    assert len(nodes) == 7

    loc = nodes['AAA']
    assert loc.name == 'AAA'

    steps = 0
    while loc.name != 'ZZZ':
        steps += 1
        for each in path:
            loc = nodes[loc.left if each == 'L' else loc.right]

    assert loc.name == 'ZZZ'
    assert steps * len(path) == 2

def test_demo1_part2():
    lines = SAMPLE_DATA2.splitlines()
    path = lines[1]
    assert path == 'LR'

    nodes = {x.name: x for x in [Node(x) for x in lines[3:]]}
    assert len(nodes) == 8

    loc = [x for x in nodes.values() if x.name[-1] == 'A']
    print(loc)
    assert len(loc) == 2

    steps = 0
    while not all([x.name[-1] == 'Z' for x in loc]):
        steps += 1
        for each in path:
            loc = [nodes[x.left if each == 'L' else x.right] for x in loc]

    assert steps * len(path) == 6

def test_day1():
    with open('day8/data1.txt') as f:
        lines = f.readlines()

    path = lines[0].strip('\n')
    nodes = {x.name: x for x in [Node(x.strip('\n')) for x in lines[2:]]}

    assert path.endswith('LLRRRR')
    assert len(path) == 277
    assert len(nodes) == 742

    loc = nodes['AAA']
    assert loc.name == 'AAA'

    steps = 0
    while loc.name != 'ZZZ':
        steps += 1
        for each in path:
            loc = nodes[loc.left if each == 'L' else loc.right]

    assert loc.name == 'ZZZ'
    assert steps * len(path) not in [79,]
    assert (steps * len(path)) == 21883

def test_day2():
    with open('day8/data1.txt') as f:
        lines = f.readlines()

    path = lines[0].strip('\n')
    nodes = {x.name: x for x in [Node(x.strip('\n')) for x in lines[2:]]}

    assert path.endswith('LLRRRR')
    assert len(path) == 277
    assert len(nodes) == 742

    loc = [x for x in nodes.values() if x.name[-1] == 'A']
    dest = [x for x in nodes.values() if x.name[-1] == 'Z']
    assert len(loc) == 6
    assert len(dest) == 6

    for v in Node.AllNodes.values():
        v.l = Node.AllNodes[v.left]
        v.r = Node.AllNodes[v.right]

    assert all([x.l is not None for x in Node.AllNodes.values()])
    assert all([x.r is not None for x in Node.AllNodes.values()])


    print([x.ends[-1] for x in loc])
    # breakpoint()
    for indx, istep in enumerate(cycle(path), 1):
        for node in loc:
            if len(node.ends) > 1 and node.ends[0] == node.ends[1] and \
                node.steps[0] != node.steps[1]:
                break
            else:
                next_node = node.ends[-1].next(istep)
                node.ends[-1] = next_node
                node.steps[-1] = indx
                if next_node.name[-1] == 'Z':
                    node.ends.append(next_node)
                    node.steps.append(indx)

        ret = [x.ends[-1].name[-1] == 'Z' for x in loc]
        # breakpoint()

        if all(ret):
            print('ALL')
            print(ret)
            print([x.ends[-1] for x in loc])
            break

        # if True in ret:
        #     print('RET')
        #     print(ret)
        #     print([x.ends[-1] for x in loc])
        #     # break

        if indx > 100000:
            print('INDX')
            print(ret)
            print([x.ends[-1] for x in loc])
            break

    print(loc)
    print([x.ends for x in loc])
    print([x.steps for x in loc])
    assert indx not in [79,]
    print([x.steps[0] for x in loc])
    assert math.lcm(*[x.steps[0] for x in loc]) == 12833235391111

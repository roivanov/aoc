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

pattern = re.compile(r'(\S+) = \((\S+), (\S+)\)')

class Node:
    def __init__(self, s) -> None:
        m = pattern.match(s)
        # print(m.groups())
        self.name, self.left, self.right = m.groups()

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

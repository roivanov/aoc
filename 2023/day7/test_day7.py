from enum import IntEnum, auto
from itertools import groupby

class Card(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    T = 10

    J = auto()
    Q = auto()
    K = auto()
    A = auto()

class HandPower(IntEnum):
    NONE = auto()
    PAIR = auto()
    TWO_PAIRS = auto()
    THREE = auto()
    FULLHOUSE = auto()
    FOUR = auto()
    FIVE = auto()

class Hand:
    def __init__(self, s: str) -> None:
        self.s = s
        self.cards = [Card[x] if x.isalpha() else Card(int(x)) for x in s]
        self.__power = {k:len(list(v)) for k,v in groupby(sorted(self.cards))}

    def power(self) -> HandPower:
        vals = sorted(self.__power.values())
        if max(vals) == 5:
            return HandPower.FIVE
        elif max(vals) == 4:
            return HandPower.FOUR
        elif set(vals) == {3, 2}:
            return HandPower.FULLHOUSE
        elif max(vals) == 3:
            return HandPower.THREE
        elif vals == [1, 2, 2]:
            return HandPower.TWO_PAIRS
        elif max(vals) == 2:
            return HandPower.PAIR
        return HandPower.NONE

    def __str__(self) -> str:
        return f"hand: {self.s}"

    def __repr__(self) -> str:
        return f"hand: {self.s} {self.power()}"

    def __lt__(self, other):
        if self.power() != other.power():
            return self.power() < other.power()
        else:
            for a, b in zip(self.s, other.s):
                if a != b:
                    return a < b

        raise RuntimeError('must not be here')

def test_part1_definitions():
    print(list(Card))
    print(Card(5))
    print(Card['A'])

    assert Card(2) < Card['A']

    print(Hand('AQJ5T2').cards)

    assert Hand('AAAAA').power() == HandPower.FIVE
    assert Hand('AA8AA').power() == HandPower.FOUR
    assert Hand('23332').power() == HandPower.FULLHOUSE
    assert Hand('TTT98').power() == HandPower.THREE
    assert Hand('23432').power() == HandPower.TWO_PAIRS
    assert Hand('KK677').power() == HandPower.TWO_PAIRS
    assert Hand('A23A4').power() == HandPower.PAIR
    assert Hand('23456').power() == HandPower.NONE

    assert Hand('33332') > Hand('2AAAA')


EXAMPLE_DATA = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

def test_part1_sample():
    hands = {}
    for line in EXAMPLE_DATA.splitlines():
        if line:
            hand_str, bid = line.split(' ')
            hand = Hand(hand_str)
            hands[hand] = int(bid)

    win = sum([hands[x] * (1+indx) for indx,x in enumerate(sorted(hands))])
    assert win == 6440


def test_part1_sample():
    print(Hand('32T3J').power(), Hand('A9942').power())
    assert Hand('32T3J') < Hand('A9942')

    assert Hand('3JKKQ').power() == HandPower.PAIR

    hands = {}
    with open('day7/data1') as f:
        for line in f.readlines()[:1006]:
            # if line:
            hand_str, bid = line.strip('\n').split(' ')
            hand = Hand(hand_str)
            hands[hand] = int(bid)

    if len(hands) < 10:
        print(', '.join([f"{x} {x.power().name} {hands[x]} * {(1+indx)}"
                        for indx,x in enumerate(sorted(hands))]))
    else:
        assert hand_str == '38383'
        assert bid == '612'


    win = sum([hands[x] * (1+indx) for indx,x in enumerate(sorted(hands))])
    prev = None
    for each in sorted(hands):
        if prev:
            assert each > prev
            prev = each

    assert win < 252410386
    assert win > 251498971
    assert len(hands) == 1000
    assert win == 1

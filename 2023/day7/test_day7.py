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
        # print(self.__power.values())
        # print(max(self.__power.values()))
        if max(self.__power.values()) == 5:
            return HandPower.FIVE
        elif max(self.__power.values()) == 4:
            return HandPower.FOUR
        elif set(self.__power.values()) == {3, 2}:
            return HandPower.FULLHOUSE
        elif max(self.__power.values()) == 3:
            return HandPower.THREE
        elif list(self.__power.values()) == [2, 2, 1]:
            return HandPower.TWO_PAIRS
        elif max(self.__power.values()) == 2:
            return HandPower.PAIR
        return HandPower.NONE


def test_part1_sample():
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
    assert Hand('A23A4').power() == HandPower.PAIR
    assert Hand('23456').power() == HandPower.NONE

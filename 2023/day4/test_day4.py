from collections import deque

class Card:
    def __init__(self, s: str) -> None:
        self.s = s.strip('\n')
        card, numbers = self.s.split(':')
        self.id = int(card.split(' ')[-1])
        a, b = numbers.strip('\n').split(':')[-1].split('|')
        lucky_numbers = {int(x) for x in a.strip().split(' ') if x}
        my_numbers = {int(x) for x in b.strip().split(' ') if x}
        self.matching_numbers_count = len(my_numbers.intersection(lucky_numbers))

    def power(self):
        return int(pow(2, self.matching_numbers_count - 1))

    def __str__(self) -> str:
        return self.s

    def __repr__(self) -> str:
        return f"Card: {self.id}"

def count(fname):
    ret = 0
    card_dict = {}
    my_cards = deque()
    with open(fname) as f:
        for line in f.readlines():
            c = Card(line)
            card_dict[c.id] = c
            my_cards.append(c.id)
            ret += c.power()

    i = 0
    done = False
    while not done:
        try:
            card_id = my_cards.pop()
            my_cards.extend(range(card_id+1,
                                card_id+1+ card_dict[card_id].matching_numbers_count))
            i+=1
        except IndexError:
            done = True

    return ret, i

def test_day4_demo():
    assert count('day4/data1') == (13, 30)

def test_day4():
    assert count('day4/data2') == (26218, 9997537)

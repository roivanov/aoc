
class Card:
    def __init__(self, s: str) -> None:
        card, numbers = s.strip('\n').split(':')
        self.id = int(card.split(' ')[-1])
        a, b = numbers.strip('\n').split(':')[-1].split('|')
        self.lucky_numbers = {int(x) for x in a.strip().split(' ') if x}
        self.my_numbers = {int(x) for x in b.strip().split(' ') if x}

    def power(self):
        return int(pow(2, len(self.my_numbers.intersection(self.lucky_numbers))-1))

def count(fname):
    ret = 0
    with open(fname) as f:
        for line in f.readlines():
            c = Card(line)
            ret += c.power()

    return ret

def test_day4():
    assert count('day4/data1') == 13
    assert count('day4/data2') == 26218

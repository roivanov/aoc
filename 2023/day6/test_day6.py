def hold(iter):
    for t, d in iter:
        print(t,d)
        count=0
        for p in range(0, t):
            s = p
            if s * (t-p) > d:
                count+=1
        yield count

def solve(fname, kerning=False):
    with open(fname) as f:
        for line in f.readlines():
            if not kerning:
                data = [int(x) for x in line.split(':')[1].strip().split()]
            else:
                data = [int(''.join([x for x in line.split(':')[1].strip() if x.isdigit()]))]
            if line.startswith('Time'):
                times = data
            elif line.startswith('Distance'):
                distance = data

    ret = 1
    for each in hold(zip(times, distance)):
        ret *= each
    return ret
            
def test_part1_sample():
    assert solve('day6/data1part1sample.txt') == 288

def test_part2_sample():
    assert solve('day6/data1part1sample.txt', kerning=True) == 71503

def test_part1_puzzle1():
    assert solve('day6/data1part1puzzle.txt') == 140220

def test_part2_puzzle1():
    assert solve('day6/data1part1puzzle.txt', kerning=True) == 140220

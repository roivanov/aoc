from itertools import chain

class Interval:
    def __init__(self, left:int, right:int) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"{self.left}<=..<{self.right}"

    def __repr__(self) -> str:
        return f"Interval: {self}"
        
    def cross(self, elfmap):
        for other in elfmap.intervals:
            assert isinstance(elfmap, ElfMap)
            print(self, 'vs', other)
            if self.within(other):
                shift = elfmap.interval_to_dest[other] - other.left
                print(f'{self} within {other} shift {shift}')
                interval = Interval(self.left + shift, self.right + shift)
                return [interval]
            elif not self.intersect(other):
                print('do not intersect')
                continue
            elif other.left <= self.left:
                """
case1
..... 57 ...... 70
53.........61.....
                """
                if other.right <= self.right:
                    shift = elfmap.interval_to_dest[other] - other.left
                    print(f'{self} crosses {other} case1, shift {shift}')
                    print(elfmap.intervals)
                    interval1 = Interval(self.left + shift, other.right + shift)
                    interval2 = Interval(other.right, self.right)
                    return [interval1] + interval2.cross(elfmap)
                else:
                    raise NotImplementedError('other case 1')
            elif self.left <= other.left:
                """
case2
.46.... 57 ......
.....56....93.....
                """
                if self.right <= other.right:
                    shift = elfmap.interval_to_dest[other] - other.left
                    print(f'{self} crosses {other} case2, shift {shift}')
                    print(elfmap.intervals)
                    interval1 = Interval(self.left, other.left)
                    interval2 = Interval(other.left, self.right)
                    return [interval1, interval2]
                else:
                    raise NotImplementedError('other case 2')

            else:
                raise NotImplementedError('intersect')

        print('intersect none')
        return [self]

    def __lt__(self, other):
        return self.left < other.left

    def within(self, other):
        return self.left >= other.left and self.right <= other.right

    def intersect(self, other):
        return not (self.right - 1 < other.left or self.left > other.right-1)


class ElfMap:
    Names = {}
    def __init__(self, name, f) -> None:
        self.name = name
        self.data = []
        self.intervals = []
        self.interval_to_dest = {}
        while True:
            line = f.readline().strip('\n')
            if not line:
                break
            else:
                self.data.append([int(x) for x in line.split()])
                self.data[-1][2] = self.data[-1][1] + self.data[-1][2]

        for x in self.data:
            interval = Interval(x[1], x[2])
            self.intervals.append(interval)
            self.interval_to_dest[interval] = x[0]
        
        self.intervals.sort()

        ElfMap.Names[self.name] = self

    def map(self, i):
        for dest, src, finish in self.data:
            if src <= i < finish:
                return dest + i - src

        return i

class ElfData:
    def __init__(self, fname) -> None:
        with open(fname) as f:
            while True:
                line = f.readline()

                if not line:
                    break

                line = line.strip('\n')
                if line.startswith('seeds:'):
                    self.seeds = [int(x) for x in line.split(':')[-1].strip().split()]
                elif line.endswith(' map:'):
                    ElfMap(line.split(' ')[0], f)

    def process(self):
        min_location = None
        for i in self.seeds:
            path = i
            for m in ['seed-to-soil', 'soil-to-fertilizer',
                    'fertilizer-to-water', 'water-to-light',
                    'light-to-temperature',
                    'temperature-to-humidity',
                    'humidity-to-location']:
                path = ElfMap.Names[m].map(path)
            min_location = min(min_location, path) if min_location else path

        return min_location

    def process_intervals(self):
        seed_intervals = sorted([Interval(self.seeds[i],
                                          self.seeds[i] + self.seeds[i+1])
                                          for i in range(0, len(self.seeds), 2)])
        print('seed_intervals: ', [str(x) for x in seed_intervals])

        for m in ['seed-to-soil', 'soil-to-fertilizer',
                'fertilizer-to-water', 'water-to-light',
                'light-to-temperature',
                'temperature-to-humidity',
                'humidity-to-location'][:7]:
            new_intervals = []
            print(m, seed_intervals)
            for seed in seed_intervals:
                new_intervals += seed.cross(ElfMap.Names[m])

            print(m, new_intervals)
            seed_intervals = sorted(new_intervals)

            print(m, seed_intervals)
        
        return seed_intervals[0].left

def test_day5_sample():
    assert ElfData('day5/data1').process() == 35
    assert ElfData('day5/data2').process() == 486613012

def test_day5_main_small():
    data = ElfData('day5/data1')
    assert data.process_intervals() == 46

def test_day5_main_big():
    data = ElfData('day5/data2')
    assert data.process_intervals() == 56931769

class ElfMap:
    Names = {}
    def __init__(self, name, f) -> None:
        self.name = name
        self.data = []
        while True:
            line = f.readline().strip('\n')
            if not line:
                break
            else:
                self.data.append([int(x) for x in line.split()])

        ElfMap.Names[self.name] = self

    def map(self, i):
        for dest, src, lenght in self.data:
            if src <= i < src + lenght:
                return dest + i - src

        return i

def test_day5_sample():
    with open('day5/data1') as f:
        while True:
            line = f.readline()

            if not line:
                break

            line = line.strip('\n')
            if line.startswith('seeds:'):
                seeds = [int(x) for x in line.split(':')[-1].strip().split()]
            elif line.endswith(' map:'):
                ElfMap(line.split(' ')[0], f)

    min_location = None
    for i in seeds:
        path = [i]
        for m in ['seed-to-soil', 'soil-to-fertilizer',
                  'fertilizer-to-water', 'water-to-light',
                  'light-to-temperature',
                  'temperature-to-humidity',
                  'humidity-to-location']:
            path.append(ElfMap.Names[m].map(path[-1]))
        print(i, path)
        min_location = min(min_location, path[-1]) if min_location else path[-1]

    assert min_location == 35
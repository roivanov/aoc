#!/bin/env python3

count=0
with open('day2-data2') as f:
    for line in f.readlines():
        game, plays = line.strip('\n').split(':', 1)
        game_id = int(game.split(' ')[-1])
        valid_gate = True
        for play in plays.split(';'):
            pairs = {k[1]:int(k[0]) for k in [x.strip().split() for x in play.split(',')]}
            # only 12 red cubes, 13 green cubes, and 14 blue cubes?
            if pairs.get('red', 0) > 12 or pairs.get('green', 0) > 13 or pairs.get('blue', 0) > 14:
                # print(pairs)
                valid_gate = False
                break
        if valid_gate:
            count += game_id

print(count)

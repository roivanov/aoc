#!/bin/env python3

RED='red'
GREEN='green'
BLUE='blue'
count=0
games_power=0

with open('day2-data2') as f:
    for line in f.readlines():
        game, plays = line.strip('\n').split(':', 1)
        game_id = int(game.split(' ')[-1])
        valid_gate = True
        max_cubes = {RED:0, GREEN:0, BLUE:0}
        for play in plays.split(';'):
            pairs = {k[1]:int(k[0]) for k in [x.strip().split() for x in play.split(',')]}
            for each in [GREEN, BLUE, RED]:
                max_cubes[each] = max(max_cubes[each], pairs.get(each, 0))

            # only 12 red cubes, 13 green cubes, and 14 blue cubes?
            if valid_gate and pairs.get(RED, 0) > 12 or pairs.get(GREEN, 0) > 13 or pairs.get(BLUE, 0) > 14:
                # print(pairs)
                valid_gate = False
                # break
        if valid_gate:
            count += game_id

        games_power += max_cubes[BLUE] * max_cubes[GREEN] * max_cubes[RED]

print(count, games_power)

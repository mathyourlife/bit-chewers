#!/usr/bin/env python3

from BitChewers.Pipe import PipeREGEX
from BitChewers import Map, Reduce
import time

cast = Map.Cast({
    'size': 'int',
    'timestamp': 'date %b %d %H:%M:%S',
})

size_stats = Reduce.BasicStats(label='domain', value='size')
time_stats = Reduce.Extremes(label='domain', value='timestamp')

kw = {
    'regex': r'^(?P<timestamp>\w+ \d+ \d{2}:\d{2}:\d{2}) .+ from=<(?P<local>[A-Za-z-=0-9\._]*)@(?P<domain>[A-Za-z-=0-9\._]*)>, size=(?P<size>\d*),',
    'ignore_case': True,
    'maps': [
        cast
    ],
    'reducers': [
        size_stats,
        time_stats,
    ]
}
pipe_lines = PipeREGEX(**kw)

for data in pipe_lines:
    #print(data)
    pass

print('From Domain\tThroughput (kB/s)')
for k, n in size_stats.stats['count'].items():
    max = time_stats.stats['max'][k]
    min = time_stats.stats['min'][k]
    try:
        rate = size_stats.stats['sum'][k] / 1024 / (max - min)
        print('{}\t{}'.format(k, rate))
    except ZeroDivisionError:
        pass


#!/usr/bin/env python3

from BitChewers.Pipe import PipeREGEX
from BitChewers import Map, Reduce

send_stats = Reduce.BasicStats(label='domain', value='size')
cast = Map.Cast({'size': 'int'})

kw = {
    'regex': r'from=<(?P<local>[A-Za-z-=0-9\._]*)@(?P<domain>[A-Za-z-=0-9\._]*)>(, size=(?P<size>\d*))?',
    'maps': [
        cast
    ],
    'reducers': [
        send_stats,
    ]
}
pipe_lines = PipeREGEX(**kw)

for data in pipe_lines:
    #print(data)
    pass

def show_top(n, data):
    for s in sorted(data.items(), key=lambda x: x[1], reverse=True)[:n]:
        print('{}\t{}'.format(s[1], s[0]))

n = 5

print('\nMessage Counts')
show_top(n, send_stats.stats['count'])

print('\nAvg Message Size')
show_top(n, send_stats.stats['avg'])

print('\nMax Message Size')
show_top(n, send_stats.stats['max'])

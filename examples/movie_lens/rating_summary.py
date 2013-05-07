#!/usr/bin/env python3

from BitChewers.Pipe import PipeCSV
from BitChewers import Map, Reduce

cast = Map.Cast({'rating': 'int'})
gender_ratings = Reduce.BasicStats(label='gender', value='rating')

kw = {
    'maps': [cast],
    'reducers': [gender_ratings],
}
pipe_csv = PipeCSV(**kw)

for data in pipe_csv:
    pass
    #print(data)

print(gender_ratings.stats['avg'])

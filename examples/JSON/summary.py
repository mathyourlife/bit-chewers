#!/usr/bin/env python3

from BitChewers.Pipe import PipeJSON
from BitChewers.JSON import Filter

kw = {
    'filters': [
        Filter.keys_exist(['Newton Meters', 'Probability'])
    ],
}
pipe_json = PipeJSON(**kw)

for data in pipe_json:
    print(data)

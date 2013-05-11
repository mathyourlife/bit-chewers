#!/usr/bin/env python3

from BitChewers.Pipe import PipeJSON
from BitChewers import Filter

kw = {
    'filters': [
        Filter.KeysExist(['Newton Meters', 'Probability'])
    ],
}
pipe_json = PipeJSON(**kw)

for data in pipe_json:
    print(data)

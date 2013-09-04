#Postfix Scrubber Example

Pipe lines from a mail.log file into the BitChewer to get stats on:
* Message Counts
* Average Message Size
* Max Message Size

##Call

```bash
tail -n 100 mail.info  | ./top_senders.py
# or
cat -n 100 mail.info  | ./top_senders.py
# or
cat -n 100 mail.info  | python3 top_senders.py
```

##Example top_sender.py

Here's a call to the sample file provided and the output.

```bash
$ cat mail.log | python3 top_senders.py 

Message Counts
4	dddd.net
2	bbbb.com
2	aaaa.com
1	eeee.io
1	ffff.io

Avg Message Size
46636.5	dddd.net
46105.0	aaaa.com
21918.0	ffff.io
21872.0	eeee.io
14143.5	bbbb.com

Max Message Size
88939	dddd.net
80506	aaaa.com
21918	ffff.io
21872	eeee.io
15837	bbbb.com
```

##Source top_senders.py
```python3
#!/usr/bin/env python3

from BitChewers.Pipe import PipeREGEX
from BitChewers import Map, Reduce

send_stats = Reduce.BasicStatsGrouping(label='domain', value='size')
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
    print(data)
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
```

##Example send_rate.py

Use the mail.log file to find who's pushing the most through the system

```bash
$ cat mail.log | ./send_rate.py 
From Domain    Throughput (kB/s)
bbbb.com	13.81201171875
aaaa.com	45.0244140625
dddd.net	20.241536458333332
```

##Source send_rate.py

```python3
#!/usr/bin/env python3

from BitChewers.Pipe import PipeREGEX
from BitChewers import Map, Reduce
import time

cast = Map.Cast({
    'size': 'int',
    'timestamp': 'date %b %d %H:%M:%S',
})

size_stats = Reduce.BasicStatsGrouping(label='domain', value='size')
time_stats = Reduce.ExtremesGrouping(label='domain', value='timestamp')

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
```

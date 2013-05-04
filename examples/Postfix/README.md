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

##Sample top_sender.py

Here's a call to the sample file provided and the output.

```bash
$ cat mail.log | python3 top_senders.py 
{'domain': 'dddd.net', 'local': '304', 'size': 41685}
{'domain': 'dddd.net', 'local': '123', 'size': 9261}
{'domain': 'aaaa.com', 'local': '44', 'size': 80506}
{'domain': 'bbbb.com', 'local': '11', 'size': 15837}
{'domain': 'dddd.net', 'local': '25', 'size': 46661}
{'domain': 'dddd.net', 'local': '920', 'size': 88939}
{'domain': 'eeee.io', 'local': '294', 'size': 21872}
{'domain': 'ffff.io', 'local': '531', 'size': 21918}
{'domain': 'aaaa.com', 'local': '664', 'size': 11704}
{'domain': 'bbbb.com', 'local': '426', 'size': 12450}

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

##Source
```python
from BitChewers.Pipe import PipeREGEX
from BitChewers import Map, Reduce

# Cast the size value from a string to an int
cast = Map.Cast({'size': 'int'})
# This is the reducer tracking stats on the size value from the regex match
send_stats = Reduce.BasicStats(label='domain', value='size')

# Setup the pipe
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

# Pull in lines.  Nothing is needed inside the loop
for data in pipe_lines:
# print(data)
    pass
```

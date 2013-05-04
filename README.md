#BitChewers

Various processing and analytic scripts

The concept is to receive lines through an iterator from standard in like
```bash
tail -n 1000 /var/log/syslog | python3 syslog_chewer.py
```
The standard in lines are pushed through a selected pipe, filter(s), map(s), and reducer(s)

##Pipes

There are 3 main pipes currently:
* PipeLines - Pulls raw lines in as strings
* PipeJSON - Pulls in raw lines and only yields valid json decoded lines
* PipeREGEX - Pulls in raw lines and only yields values from a user supplied regex

##Example - Scrub Postfix mail.log log

[Example Postfix Scrubber](https://github.dev.mht.dyndns.com/dcouture/bit-chewers/tree/master/examples/Postfix)

```python
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

##Install

Make BitChewers available for all scripts on the box

```bash
sudo python3 setup.py install
```

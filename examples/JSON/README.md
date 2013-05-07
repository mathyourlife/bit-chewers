#JSON Example

Pipe lines from a file containing json encoded strings.
Search for strings that have both a valid json document and specified
non-null keys

##Call

```bash
head -n 400 json_lines.txt | python3 summary.py
# OR
cat json_lines.txt | ./summary.py
```

##Output

Here's a call to the sample file provided and the output.

```bash
$ head -n 400 json_lines.txt | python3 summary.py 
{'Username': 'sender@math.io', 'Count': 2, 'Probability': 86.0, 'Asteroids': 2, 'Newton Meters': 9.83, 'PlanetId': 167, 'Derivative': 1535316, 'Circular References': 2, 'Mission Num': 47}
{'Username': 'sender@math.io', 'Count': 1, 'Probability': 45.0, 'Asteroids': 1, 'Newton Meters': 7.06, 'PlanetId': 943, 'Derivative': 7877450, 'Circular References': 1, 'Mission Num': 280}
{'Username': 'sender@math.io', 'Count': 171, 'Probability': 85.0, 'Asteroids': 650, 'Newton Meters': 5.98, 'PlanetId': 1065, 'Derivative': 3268346, 'Circular References': 109, 'Mission Num': 170}
{'Username': 'sender@math.io', 'Count': 3, 'Probability': 99.0, 'Asteroids': 3, 'Newton Meters': 6.28, 'PlanetId': 1084, 'Derivative': 3606093, 'Circular References': 1, 'Mission Num': 84}
{'Username': 'sender@math.io', 'Count': 0, 'Probability': 70.0, 'Asteroids': 10, 'Newton Meters': 6.84, 'PlanetId': 1102, 'Derivative': 228891, 'Circular References': 0, 'Mission Num': 102}
```

##Source
```python
#!/usr/bin/env python3

from BitChewers.Pipe import PipeJSON
from BitChewers import Filter

kw = {
    'filters': [
        Filter.keys_exist(['Newton Meters', 'Probability'])
    ],
}
pipe_json = PipeJSON(**kw)

for data in pipe_json:
    print(data)
```

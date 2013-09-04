#Movie Rating Analysis

Taking a test data set from the MovieLens ratings http://www.grouplens.org/node/73 survey to
determine if gender plays a role in movie ratings.  Instead of modifying the script each time to
grab a separate subset, create a generic script that will analyze any data piped into it and
use the grep command to push in selected data sets.


##Data structure

csv has first line headers and the following data records
```bash
$ head -n 3 movielens_train.csv 
,user_id,movie_id,rating,timestamp,gender,age,occupation,zip,title,genres,for_testing
593263,3562,3798,4,967332344,F,25,6,32812,What Lies Beneath (2000),Thriller,False
235597,1051,3793,4,974958593,F,25,0,60513,X-Men (2000),Action|Sci-Fi,False
```

##rating_summary.py
```python3
#!/usr/bin/env python3

from BitChewers.Pipe import PipeCSV
from BitChewers import Map, Reduce

cast = Map.Cast({'rating': 'int'})
gender_ratings = Reduce.BasicStatsGrouping(label='gender', value='rating')

kw = {
    'maps': [cast],
    'reducers': [gender_ratings],
}
pipe_csv = PipeCSV(**kw)

for data in pipe_csv:
    pass
    #print(data)

print(gender_ratings.stats['avg'])
```

##Usage

Pass in various subsets of the data.  Note: the `egrep 'rating|******'` command is used to keep the header line displayed along with the subset of data.

###All reviews

```bash
$ cat movielens_train.csv | ./rating_summary.py 
{'F': 4.0, 'M': 3.731707317073171}
```

###Sci-Fi
```bash
$ egrep 'rating|Sci-Fi' movielens_train.csv | ./rating_summary.py 
{'F': 3.0, 'M': 3.7}
```

###Movies produced in 2000
```bash
$ egrep 'rating|(2000)' movielens_train.csv | ./rating_summary.py 
{'F': 4.0, 'M': 4.0}
```

###Drama
```bash
$ egrep 'rating|Drama' movielens_train.csv | ./rating_summary.py 
{'F': 4.25, 'M': 3.875}
```

#!/usr/bin/bash

python3 generator.py | python3 control_chart.py 2> /dev/null

#!/usr/bin/python3

from BitChewers.Pipe import PipeJSON
from BitChewers import Monitor
import matplotlib.pyplot as plt

def main():

    # Create a new matplotlib figure with interactive mode
    plt.ion()
    fig = plt.figure()

    # Tell the control chart we'll be monitoring the "value" field and
    # plotting it agains the "timestamp" value
    value_cc = Monitor.ControlCharts(x='timestamp', y='value', fig=fig, window_len=60)
    kwargs = {
        'monitors': [value_cc]
    }
    # The PipeJSON object pulls from stdin and pushes any valid json objects
    # through the value_cc control chart
    pj = PipeJSON(**kwargs);

    # Itterate through the incoming data.
    for line_data in pj:
        # Additional logic can go here to inspect each data point coming
        # through.
        print("Just saw a value of {value} generated at {timestamp}".format(**line_data))
        pass

if __name__ == '__main__':
    main()


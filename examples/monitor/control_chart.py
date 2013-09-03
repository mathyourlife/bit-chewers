
from BitChewers.Pipe import PipeJSON
from BitChewers import Monitor
import matplotlib.pyplot as plt

def main():

    plt.ion()
    fig = plt.figure()

    value_cc = Monitor.ControlCharts(x='timestamp', y='value', fig=fig, window_len=60)
    kwargs = {
        'monitors': [value_cc]
    }
    pj = PipeJSON(**kwargs);

    for line_data in pj:
        pass

if __name__ == '__main__':
    main()


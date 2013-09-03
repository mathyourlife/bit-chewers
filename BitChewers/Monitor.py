"""
Monitor values pulled in through a pipe.
"""

import matplotlib.pyplot as plt
import numpy as np


class ControlCharts(object):
    """
    A control chart to track a rolling window of data values.
    """

    def __init__(self, x, y, fig, window_len=None):
        if window_len is None:
            window_len = 10

        self.window_len = window_len
        self.x_key = x
        self.y_key = y
        self.idx = 0

        self.fig = fig
        self.ax = fig.add_subplot(111)
        self.l, = self.ax.plot([], [], 'r-o')

        self.cl = []
        for s in range(-3, 4):
            self.cl.append({
                "sigma": s,
                "line": self.ax.axhline(linestyle='--', alpha=0.3),
                "text": self.ax.text(x=0, y=0, s='', alpha=0.5),
            })

        self.x = np.array([np.nan] * window_len, dtype=np.float)
        self.y = np.array([np.nan] * window_len, dtype=np.float)

    def monitor(self, data):
        """
        Push a new data point to the monitor plot

        :param data: structure of data to monitor
        :type data: dict
        """

        self.x[self.idx] = data[self.x_key]
        self.y[self.idx] = data[self.y_key]

        xdata = np.hstack((self.x[self.idx+1:], self.x[:self.idx+1]))
        ydata = np.hstack((self.y[self.idx+1:], self.y[:self.idx+1]))

        self.l.set_xdata(xdata)
        self.l.set_ydata(ydata)

        xmin = self.x[~np.isnan(self.x)].min()
        xmax = self.x[~np.isnan(self.x)].max() + 1
        plt.xlim(xmin, xmax)

        y_mean = self.y[~np.isnan(self.y)].mean()
        y_stdev = self.y[~np.isnan(self.y)].std()

        ymin = np.min((
                self.y[~np.isnan(self.y)].min(),
                y_mean - 3 * y_stdev
            ))
        ymax = np.max((
                self.y[~np.isnan(self.y)].max() + 1,
                y_mean + 3 * y_stdev
            ))
        plt.ylim(ymin, ymax)

        for cl in self.cl:
            y_val = y_mean + y_stdev * cl['sigma']
            cl['line'].set_ydata([y_val, y_val])

            cl['text'].set_position((
                np.min(xdata[~np.isnan(xdata)]),
                y_val
            ))
            cl['text'].set_text('%+d=%g' % (cl['sigma'], y_val))

        self.fig.canvas.draw()

        if self.idx >= self.window_len - 1:
            self.idx = 0
        else:
            self.idx += 1


"""
Reducing operations.  Performed after pipe in from stdin
then filtered, then mapped.
"""

from collections import defaultdict


class BaseReduce(object):
    def reduce(self, data):
        pass

    def finish(self):
        pass

class Count(BaseReduce):
    """
    A basic counting class.  Track the number of occurances of a key.
    """
    def __init__(self, key):
        self.key = key
        self.counts = defaultdict(int)

    def reduce(self, data):
        """
        Reducing function that increments the needed key
        """
        self.counts[data[self.key]] += 1


class Min(BaseReduce):
    """
    Determine the min value encoutered grouped by the label field.
    """
    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.min = {}

    def reduce(self, data):
        """
        Reducing function to reduce the recorded min if found
        """

        if data[self.label] not in self.min:
            self.min[data[self.label]] = data[self.value]
            return

        if data[self.value] < self.min[data[self.label]]:
            self.min[data[self.label]] = data[self.value]


class Max(BaseReduce):
    """
    Determine the max value encoutered grouped by the label field.
    """
    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.max = {}

    def reduce(self, data):
        """
        Reducing function to bump up the recorded max if found
        """

        if data[self.label] not in self.max:
            self.max[data[self.label]] = data[self.value]
            return

        if data[self.value] > self.max[data[self.label]]:
            self.max[data[self.label]] = data[self.value]


class Extremes(BaseReduce):
    """
    Track min and max for the groups.
    """

    def __init__(self, key):
        self.key = key
        self.stats = {
            'min': None,
            'max': None,
        }

    def reduce(self, data):
        """
        Reducing function to track extremes
        """

        if self.stats['min'] is None:
            self.stats['min'] = data[self.key]
            self.stats['max'] = data[self.key]
            return

        if data[self.key] < self.stats['min']:
            self.stats['min'] = data[self.key]
            return

        if self.stats['max'] < data[self.key]:
            self.stats['max'] = data[self.key]


class ExtremesGrouping(BaseReduce):
    """
    Track min and max for the groups.
    """

    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.stats = {
            'min': {},
            'max': {},
        }

    def reduce(self, data):
        """
        Reducing function to track extremes
        """

        if data[self.label] not in self.stats['min']:
            # First instance of this label
            self.stats['min'][data[self.label]] = data[self.value]
            self.stats['max'][data[self.label]] = data[self.value]
        else:
            # Set the min
            if data[self.value] < self.stats['min'][data[self.label]]:
                self.stats['min'][data[self.label]] = data[self.value]
            # Set the max
            if data[self.value] > self.stats['max'][data[self.label]]:
                self.stats['max'][data[self.label]] = data[self.value]


class BasicStats(BaseReduce):
    """
    Limited stats that don't require a history to compute.
    """

    def __init__(self, key):
        self.key = key
        self.stats = {
            'min': None,
            'max': None,
            'count': 0,
            'sum': 0,
            'avg': None,
        }

    def reduce(self, data):
        """
        Reducing function to track basic stats
        """

        self.stats['count'] += 1
        self.stats['sum'] += data[self.key]

        if self.stats['count'] == 1:
            self.stats['min'] = data[self.key]
            self.stats['max'] = data[self.key]
            self.stats['sum'] = data[self.key]

        if data[self.key] < self.stats['min']:
            self.stats['min'] = data[self.key]
            return

        if self.stats['max'] < data[self.key]:
            self.stats['max'] = data[self.key]

    def finish(self):
        """
        For stats that are completed at the end of the run
        """
        self.stats['avg'] = self.stats['sum'] / self.stats['count']


class BasicStatsGrouping(BaseReduce):
    """
    Limited stats that don't require a history to compute.
    """

    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.stats = {
            'min': {},
            'max': {},
            'count': defaultdict(int),
            'sum': {},
            'avg': {},
        }

    def reduce(self, data):
        """
        Reducing function to track basic stats
        """

        # Increment the count
        self.stats['count'][data[self.label]] += 1

        if data[self.label] not in self.stats['min']:
            # First instance of this label
            self.stats['min'][data[self.label]] = data[self.value]
            self.stats['max'][data[self.label]] = data[self.value]
            self.stats['sum'][data[self.label]] = data[self.value]
        else:
            # Add to Running total
            self.stats['sum'][data[self.label]] += data[self.value]

            # Set the min
            if data[self.value] < self.stats['min'][data[self.label]]:
                self.stats['min'][data[self.label]] = data[self.value]
            # Set the max
            if data[self.value] > self.stats['max'][data[self.label]]:
                self.stats['max'][data[self.label]] = data[self.value]

    def finish(self):
        """
        For stats that are completed at the end of the run
        """

        for k in self.stats['count'].keys():
            self.stats['avg'][k] = self.stats['sum'][k] / self.stats['count'][k]

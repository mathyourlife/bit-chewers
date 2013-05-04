"""
Reducing operations.  Performed after pipe in from stdin
then filtered, then mapped.
"""

from collections import defaultdict

class Map:
    def reduce(self, data):
        pass

    def finish(self, data):
        pass

class Count(Map):
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

class Max(Map):
    """
    Determine the max value encoutered grouped by the label field.
    """
    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.max = defaultdict(int)

    def reduce(self, data):
        """
        Reducing function to bump up the recorded max if found
        """
        if data[self.value] > self.max[data[self.label]]:
            self.max[data[self.label]] = data[self.value]

class BasicStats(Map):
    """
    Limited stats that don't require a history to compute.
    """

    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.stats = {
            'max': defaultdict(int),
            'count': defaultdict(int),
            'sum': defaultdict(int),
            'avg': defaultdict(int),
        }

    def reduce(self, data):
        """
        Reducing function to track basic stats
        """

        # Increment the count
        self.stats['count'][data[self.label]] += 1

        # Add to Running total
        self.stats['sum'][data[self.label]] += data[self.value]

        # Set the max
        if data[self.value] > self.stats['max'][data[self.label]]:
            self.stats['max'][data[self.label]] = data[self.value]

    def finish(self):
        """
        For stats that are completed at the end of the run
        """

        for k in self.stats['count'].keys():
            self.stats['avg'][k] = self.stats['sum'][k] / self.stats['count'][k]

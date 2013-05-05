"""
Iterator classes meant to take input piped in from an external
source, do some initial validation/filtering on it then
yield values a line at a time until the end of the input.

# Yield lines
p = PipeLines()
# Yield valid json objects
p = PipeJSON()
# Yield regex matches
p = PipeREGEX(regex=r'([a-z]+)\s([a-z]+)', ignore_case=True)

for line in p:
    print(line)
"""

import sys
import json
import re


class PipeLines:
    """
    Pipe standard string lines in and create an iterator
    """

    def __init__(self, filters=None, maps=None, reducers=None):
        self.filters = filters
        self.maps = maps
        self.reducers = reducers

    def __iter__(self):
        """
        Return the instantiated object as the iterator
        """
        return self

    def __next__(self):
        """
        Method called by the iterator to produce the next value

        :return: The next valid string pulled in from stdin
        :rtype: str
        """

        line = [self.from_stdin()]

        # Keep pulling while the lines don't pass validation/filtering
        while not self.validate(line):
            line = [self.from_stdin()]

        return line[0]

    def from_stdin(self):
        """
        Supporting method to grab the next line from stdin

        :return: Next line from stdin
        :rtype: str
        """

        line = sys.stdin.readline()
        if len(line) == 0:
            self.finish_reduce()
            raise StopIteration
        return line

    def validate(self, line):
        """
        Determine if the input string is valid to pass on.  Inital
        validation for raw input followed by optional filtering supplied
        by the user.

        :return: True if okay, False if skip
        :rtype: bool
        """

        if not self.filter(line):
            return False

        self.map(line)
        self.reduce(line)

        return True

    def filter(self, line):
        """
        The line has passed initial validation and needs to be subjected
        to additional filtering for a user.

        :return: True if passes all the user supplied filtering
        :rtype: bool
        """

        if self.filters is None:
            return True

        if all(f.validate(line[0]) for f in self.filters):
            return True

        return False

    def map(self, line):
        """
        Alter the filtered line by a user defined map
        """

        if self.maps is None:
            return

        for m in self.maps:
            m.map(line)

    def reduce(self, line):
        """
        Run the filtered line through any reducing function defined by
        the user
        """

        if self.reducers is None:
            return

        for r in self.reducers:
            r.reduce(line[0])

    def finish_reduce(self):
        """
        End of line input.  Finish of the reducers.
        """

        if self.reducers is None:
            return

        for r in self.reducers:
            r.finish()


class PipeJSON(PipeLines):
    """
    Iterator from stdin pipe that yields dict from valid json encoded lines.
    Line passed in as a list so it can be mutated
    """

    def validate(self, line):
        """
        Determine if the input string is valid to pass on.  Inital
        validation for raw input followed by optional filtering supplied
        by the user.

        :return: True if okay, False if skip
        :rtype: bool
        """
        try:
            line[0] = json.loads(line[0])
        except ValueError:
            return False

        if not self.filter(line):
            return False

        return True


class PipeREGEX(PipeLines):
    """
    Iterator from stdin pipe that yields tuples.
    Line passed in as a list so it can be mutated.  Lines are
    yielded as tuples of matched data.
    """

    def __init__(self, regex, ignore_case=False, filters=None,
                 maps=None, reducers=None):
        """
        Set up the regex to test against all lines being piped in.

        :param regex: The regex string to compile
        :type regex: str

        :param ignore_case: Should match be case insensitve?
        :type ignore_case: bool
        """

        super().__init__(filters=filters, maps=maps, reducers=reducers)
        if ignore_case:
            self.regex = re.compile(regex, re.IGNORECASE)
        else:
            self.regex = re.compile(regex)

    def validate(self, line):
        """
        Determine if the input string is valid to pass on.  Inital
        validation for raw input followed by optional filtering supplied
        by the user.

        :return: True if okay, False if skip
        :rtype: bool
        """

        m = self.regex.search(line[0])
        if m is None:
            return False
        line[0] = m.groupdict()

        if not self.filter(line):
            return False

        self.map(line)
        self.reduce(line)

        return True

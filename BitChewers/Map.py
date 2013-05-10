"""
Tools to  map input object to new output representations.
"""

import datetime
import time


class Cast:
    """
    Filter out values that do not contain the correct keys
    """
    def __init__(self, cast):
        self.cast = cast

    def map(self, data):
        """
        Verify that the data in has the specified keys.

        :param data: dict to check for key existance
        :type data: dict

        :return: If the data has all the keys populated
        :rtype: bool
        """

        for k, type in self.cast.items():
            if type == 'int':
                try:
                    data[0][k] = int(data[0][k])
                except TypeError:
                    data[0][k] = 0
            elif type[0:4] == 'date':
                data[0][k] = time.mktime(datetime.datetime.strptime(data[0][k], type[5:]).timetuple())
            else:
                raise NotImplementedError

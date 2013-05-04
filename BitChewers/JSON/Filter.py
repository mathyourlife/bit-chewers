"""
Tools to filter our logs containing json objects.
"""


class keys_exist:
    """
    Filter out values that do not contain the correct keys
    """
    def __init__(self, keys):
        self.keys = keys

    def validate(self, data):
        """
        Verify that the data in has the specified keys.

        :param data: dict to check for key existance
        :type data: dict

        :return: If the data has all the keys populated
        :rtype: bool
        """
        for k in self.keys:
            if k not in data or data[k] is None:
                return False
        return True

import unittest

from BitChewers import Map
import time

class CastTest(unittest.TestCase):

    def test_basic(self):
        cast = {
            'time': 'int'
        }
        obj = Map.Cast(cast)

        data = [{'time': '345'}]

        obj.map(data)

        self.assertNotEqual([{'time': '345'}], data)
        self.assertEqual([{'time': 345}], data)

    def test_mulitcast(self):
        cast = {
            'time': 'int',
            'value': 'int'
        }

        obj = Map.Cast(cast)

        data = [{
            'time': '567',
            'value': 3.56
        }]

        obj.map(data)

        self.assertEqual([{
            'time': 567,
            'value': 3
        }], data)

    def test_extra_keys(self):
        cast = {
            'time': 'int'
        }

        obj = Map.Cast(cast)

        data = [{
            'time': '567',
            'value': 'yes'
        }]

        obj.map(data)

        self.assertEqual([{
            'time': 567,
            'value': 'yes'
        }], data)

    def test_time(self):
        cast = {
            'timestamp': 'date %d %b %y'
        }

        obj = Map.Cast(cast)

        data = [{
            'timestamp': '05 May 13'
        }]

        obj.map(data)

        self.assertEqual([{
            'timestamp': 1367726400.0
        }], data)

    def test_not_implemented(self):
        cast = {
            'time': 'float'
        }

        obj = Map.Cast(cast)

        data = [{
            'time': '345.6'
        }]

        with self.assertRaises(NotImplementedError):
            obj.map(data)


if __name__ == '__main__':
    unittest.main()

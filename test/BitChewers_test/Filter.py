import unittest

from BitChewers import Filter

class KeysExistTest(unittest.TestCase):

    def test(self):
        keys = ['a', 'b']

        obj = Filter.KeysExist(keys)

        data = {'a': '1', 'b': 2}
        result = obj.validate(data)
        self.assertEqual(True, result)

    def test_missing(self):
        keys = ['a', 'b']

        obj = Filter.KeysExist(keys)

        data = {'a': '1', 'b': None}
        result = obj.validate(data)
        self.assertEqual(False, result)

        data = {'a': '1', 'c': 3}
        result = obj.validate(data)
        self.assertEqual(False, result)


if __name__ == '__main__':
    unittest.main()

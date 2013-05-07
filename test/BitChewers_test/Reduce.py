import unittest

from BitChewers import Reduce


class BaseReduceTest(unittest.TestCase):
    """ Base Reduce Class tests """

    def test(self):
        obj = Reduce.BaseReduce()

        data = {'time': '345'}

        obj.reduce(data)
        obj.finish()

        self.assertEqual({'time': '345'}, data)


class CountTest(unittest.TestCase):
    """ Verify we can count the occurances of labels """

    def test(self):
        obj = Reduce.Count('group')

        data_a = {'group': 'a'}
        data_b = {'group': 'b'}
        data_c = {'group': 'c'}

        obj.reduce(data_a)
        obj.reduce(data_a)
        obj.reduce(data_b)
        obj.reduce(data_b)
        obj.reduce(data_c)

        self.assertEqual(2, obj.counts['a'])
        self.assertEqual(2, obj.counts['b'])
        self.assertEqual(1, obj.counts['c'])
        self.assertEqual(0, obj.counts['d'])


class MinTest(unittest.TestCase):
    """ Verify we can track the min value by label """

    def test(self):
        obj = Reduce.Min(label='group', value='number')

        data = [
            {'group': 'a', 'number': 4},
            {'group': 'a', 'number': -20},
            {'group': 'a', 'number': 10.3},
        ]

        for d in data:
            obj.reduce(d)

        self.assertEqual(-20, obj.min['a'])

    def test_multi(self):
        obj = Reduce.Min(label='group', value='number')

        data = [
            {'group': 'a', 'number': 4},
            {'group': 'b', 'number': 4},
            {'group': 'c', 'number': -20},
            {'group': 'a', 'number': 10.3},
            {'group': 'b', 'number': -20},
            {'group': 'c', 'number': 10.3},
        ]

        for d in data:
            obj.reduce(d)

        self.assertEqual(4, obj.min['a'])
        self.assertEqual(-20, obj.min['b'])
        self.assertEqual(-20, obj.min['c'])


class MaxTest(unittest.TestCase):
    """ Verify we can track the max value by label """

    def test(self):
        obj = Reduce.Max(label='group', value='number')

        data = [
            {'group': 'a', 'number': 4},
            {'group': 'a', 'number': -20},
            {'group': 'a', 'number': 10.3},
        ]

        for d in data:
            obj.reduce(d)

        self.assertEqual(10.3, obj.max['a'])

    def test_multi(self):
        obj = Reduce.Max(label='group', value='number')

        data = [
            {'group': 'a', 'number': 4},
            {'group': 'b', 'number': 4},
            {'group': 'c', 'number': -20},
            {'group': 'a', 'number': 10.3},
            {'group': 'b', 'number': -20},
            {'group': 'c', 'number': 10.3},
        ]

        for d in data:
            obj.reduce(d)

        self.assertEqual(10.3, obj.max['a'])
        self.assertEqual(4, obj.max['b'])
        self.assertEqual(10.3, obj.max['c'])


class BasicStatsTest(unittest.TestCase):
    """ Verify we can track the max value by label """

    def test(self):
        obj = Reduce.BasicStats(label='group', value='number')

        data = [
            {'group': 'a', 'number': 4},
            {'group': 'a', 'number': -20},
            {'group': 'a', 'number': 10.5},
            {'group': 'a', 'number': 8},
        ]

        for d in data:
            obj.reduce(d)

        obj.finish()

        self.assertEqual(4, obj.stats['count']['a'])
        self.assertEqual(-20, obj.stats['min']['a'])
        self.assertEqual(10.5, obj.stats['max']['a'])
        self.assertEqual(2.5, obj.stats['sum']['a'])
        self.assertEqual(0.625, obj.stats['avg']['a'])


if __name__ == '__main__':
    unittest.main()

import unittest
import datetime

from dss.TimeFormatFactory import TimeFormatFactory

class TestTimeFormatFactory(unittest.TestCase):
    def setUp(self):
        self.time_factory = TimeFormatFactory()

    def test_create_string(self):
        new_time = datetime.datetime(2015, 5, 20, 20, 20, 20)
        time_func = self.time_factory.get_time_func('string')
        time_str = time_func(new_time)
        self.assertEqual(time_str, '2015-05-20 20:20:20')

    def test_create_timestamp(self):
        new_time = datetime.datetime(2015, 5, 20, 20, 20, 20)
        time_func = self.time_factory.get_time_func('timestamp')
        time_stamp = time_func(new_time)
        self.assertEqual(time_stamp, 1432124420.0)


if __name__ == '__main__':
    unittest.main()

import unittest
from io import StringIO
from spacelib.types import FlightProperty
from spacelib.telemetry import sensors


class TestCollector(unittest.TestCase):
    def test_hasattr(self):
        self.assertTrue(hasattr(FlightProperty, 'bedrock_altitude'))
        self.assertFalse(hasattr(FlightProperty, ''))
        self.assertFalse(hasattr(FlightProperty, 'Nothing'))


    def test_save_flight_data(self):
        data = {
            'a': [1, 2, 3],
            'b': [(1,2), (3,4), (5,6)],
            'c': ['a', 'b', 'c'],
            'time': [1.1, 1.2, 1.3],
        }
        expected = [";a;b;c;time",
                    "0;1;(1, 2);a;1.1",
                    "1;2;(3, 4);b;1.2",
                    "2;3;(5, 6);c;1.3"]
        with StringIO() as file:
            sensors.save_flight_data(file, data)
            file.seek(0)
            output = file.read().splitlines()
            self.assertEqual(expected, output)
        
        
if __name__ == '__main__':
    unittest.main()

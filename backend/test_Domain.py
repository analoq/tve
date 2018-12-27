import unittest
from datetime import datetime

from Domain import Domain

class TestDomain(unittest.TestCase):
    def test_round_minute(self):
        dt0 = datetime(2018, 12, 25, 12, 34, 56)
        f = datetime(2018, 12, 25, 12, 0, 0)
        c = datetime(2018, 12, 25, 13, 0, 0)
        self.assertEqual(Domain.round_hour(dt0), c)

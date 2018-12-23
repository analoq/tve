import unittest
import os
from datetime import datetime, timedelta

from Persistence import Persistence


class TestPersistence(unittest.TestCase):
    def setUp(self):
        self.persistence = Persistence('test.db')

    def tearDown(self):
        if os.path.exists('test.db'):
            os.remove('test.db')

    def test_init(self):
        self.assertEqual(os.path.exists('test.db'), True)

    def test_historical(self):
        dt0 = datetime.utcnow() - timedelta(seconds=120)
        dt1 = datetime.utcnow() - timedelta(seconds=30)
        dt2 = datetime.utcnow() - timedelta(seconds=15)
        self.persistence.store(dt0, 100)
        self.persistence.store(dt1, 200)
        self.persistence.store(dt2, 300)
        result = self.persistence.historical(60)
        expected = [
            {'dt': dt1, 'value': 200},
            {'dt': dt2, 'value': 300}
        ]
        self.assertEqual(expected, result)

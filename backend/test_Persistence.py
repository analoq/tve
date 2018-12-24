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
        now = datetime.utcnow().replace(microsecond=0)
        dt0 = now - timedelta(seconds=120)
        dt1 = now - timedelta(seconds=30)
        dt2 = now - timedelta(seconds=15)
        self.persistence.store(dt0, 100)
        self.persistence.store(dt1, 200)
        self.persistence.store(dt2, 300)
        result = self.persistence.historical(60)
        expected = [
            {'dt': dt1, 'value': 200},
            {'dt': dt2, 'value': 300}
        ]
        self.assertEqual(result, expected)

    def test_historical_archive(self):
        now = datetime.utcnow().replace(minute=0,second=0,microsecond=0)
        dt0 = now - timedelta(minutes=50)
        dt1 = now - timedelta(minutes=10)
        dt2 = now - timedelta(minutes=5)
        self.persistence.store(dt0, 100)
        self.persistence.store(dt1, 200)
        self.persistence.store(dt2, 300)
        self.persistence.archive()
        result = self.persistence.historical_archive(10)
        expected = [
            {'dt': dt0.replace(minute=0), 'value': 100},
            {'dt': dt1.replace(minute=45), 'value': 250},
        ]
        self.assertEqual(result, expected)

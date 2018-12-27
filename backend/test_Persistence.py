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
        self.persistence.store(dt0, 0.1, 0.1, 0.1, 0.1)
        self.persistence.store(dt1, 0.2, 0.2, 0.2, 0.2)
        self.persistence.store(dt2, 0.3, 0.3, 0.3, 0.3)
        result = self.persistence.historical(60)
        expected = [
            {'dt': dt1, 'moisture': 0.2, 'luminence': 0.2, 'temperature': 0.2, 'humidity': 0.2},
            {'dt': dt2, 'moisture': 0.3, 'luminence': 0.3, 'temperature': 0.3, 'humidity': 0.3}
        ]
        self.assertEqual(result, expected)

    def test_historical_archive(self):
        now = datetime.utcnow().replace(minute=0,second=0,microsecond=0)
        dt0 = now - timedelta(minutes=80)
        dt1 = now - timedelta(minutes=70)
        dt2 = now - timedelta(minutes=30)
        self.persistence.store(dt0, 0.0, 0.0, 0.0, 0.0)
        self.persistence.store(dt1, 0.2, 0.2, 0.2, 0.2)
        self.persistence.store(dt2, 0.3, 0.3, 0.3, 0.3)
        expected = [
            {'dt': dt1.replace(minute=0), 'moisture': 0.1, 'luminence': 0.1, 'temperature': 0.1, 'humidity': 0.1},
            {'dt': dt2.replace(minute=0), 'moisture': 0.3, 'luminence': 0.3, 'temperature': 0.3, 'humidity': 0.3},
        ]
        self.persistence.archive()
        result = self.persistence.historical_archive(3)
        self.assertEqual(result, expected)

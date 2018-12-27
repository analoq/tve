import unittest
import os
from datetime import datetime, timedelta

from Service import Service
from Persistence import Persistence


class TestService(unittest.TestCase):
    def tearDown(self):
        if os.path.exists('test.db'):
            os.remove('test.db')

    @staticmethod
    def start_response(status, headers):
        pass

    def test_request(self):
        persistence = Persistence('test.db')
        now = datetime.utcnow().replace(microsecond=0)
        dt0 = now - timedelta(seconds=30)
        persistence.store(dt0, 100.0, 100.0, 100.0, 100.0)
        service = Service(persistence)
        response = service.request(self.start_response)
        self.assertEqual(response.next(),
                'data: {"dest": "archive", "items": [], "type": "preload"}\n\n')
        self.assertEqual(response.next(),
                'data: {"dest": "recent", "items": [{"dt": "%sZ", "humidity": 100.0, "temperature": 100.0, "moisture": 100.0, "luminence": 100.0}], "type": "preload"}\n\n' % dt0.isoformat())
        dt1 = now
        service.enqueue('recent', 'realtime', [{'dt': dt1, 'moisture': 200.0, 'luminence': 200.0, 'temperature': 200.0, 'humidity': 200.0}])
        self.assertEqual(response.next(),
                'data: {"dest": "recent", "items": [{"dt": "%sZ", "humidity": 200.0, "temperature": 200.0, "moisture": 200.0, "luminence": 200.0}], "type": "realtime"}\n\n' % dt1.isoformat())


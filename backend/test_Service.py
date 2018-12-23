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
        dt0 = datetime.utcnow() - timedelta(seconds=30)
        persistence.store(dt0, 100)
        service = Service(persistence)
        response = service.request(self.start_response)
        self.assertEqual(response.next(),
                'data: [{"dt": "%s", "value": 100}]\n\n' % dt0.isoformat())
        dt1 = datetime.utcnow()
        service.enqueue({'dt': dt1, 'value': 200})
        self.assertEqual(response.next(),
                'data: [{"dt": "%s", "value": 200}]\n\n' % dt1.isoformat())


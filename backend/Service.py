"""Service module encompasses all web-service concerns"""
import logging
import json
import threading
from Queue import Queue, Empty

class Service(object):
    """Web-service class"""
    def __init__(self, persistence):
        """Initialize Service object, depends on a Persistence object"""
        self.queues = []
        self.queue_lock = threading.Lock()
        self.persistence = persistence

    @staticmethod
    def _format(sample_dest, sample_type, items):
        payload = {
            'dest': sample_dest,
            'type': sample_type,
            'items': []
        }
        for item in items:
            payload['items'].append({
                'dt': item['dt'].strftime('%Y-%m-%dT%H:%M:%SZ'),
                'moisture': item['moisture'],
                'luminence': item['luminence'],
                'temperature': item['temperature'],
                'humidity': item['humidity'],
            })
        return "data: %s\n\n" % json.dumps(payload)

    def enqueue(self, sample_dest, sample_type, items):
        """Enqueue a sample for all active clients"""
        for queue in self.queues:
            queue.put((sample_dest, sample_type, items))

    def request(self, start_response):
        """Handle a web client"""
        # initialize queue
        queue = Queue()
        self.queue_lock.acquire()
        self.queues.append(queue)
        self.queue_lock.release()
        logging.info("Starting request, queues: %d" % len(self.queues))

        # start response
        headers = [('Content-type', 'text/event-stream'),
                   ('Access-Control-Allow-Origin', '*')]
        start_response('200 OK', headers)

        # send archived samples
        items = self.persistence.historical_archive(hours=24*7)
        payload = self._format('archive', 'preload', items)
        logging.info("Archived payload: %s" % payload.strip())
        yield payload

        # send recent samples
        items = self.persistence.historical(seconds=60)
        payload = self._format('recent', 'preload', items)
        logging.info("Recent payload: %s" % payload.strip())
        yield payload

        # send samples as they arrive
        try:
            while True:
                sample_dest, sample_type, items = queue.get(timeout=60)
                payload = self._format(sample_dest, sample_type, items)
                logging.info("Sample payload: %s" % payload.strip())
                yield payload
        except (IOError, Empty) as exc:
            self.queue_lock.acquire()
            self.queues.remove(queue)
            self.queue_lock.release()
            logging.warn("Exception during request: %s" % exc)
        logging.info("Request completed")

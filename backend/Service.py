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
    def _format(items):
        payload = []
        for item in items:
            payload.append({
                'dt': item['dt'].isoformat(),
                'value': item['value'],
            })
        return "data: %s\n\n" % json.dumps(payload)

    def enqueue(self, item):
        """Enqueue a sample for all active clients"""
        for queue in self.queues:
            queue.put(item)

    def request(self, start_response):
        """Handle a web client"""
        queue = Queue()
        self.queue_lock.acquire()
        self.queues.append(queue)
        self.queue_lock.release()
        logging.info("Starting request, queues: %d" % len(self.queues))
        items = self.persistence.historical(seconds=60)

        headers = [('Content-type', 'text/event-stream'),
                   ('Access-Control-Allow-Origin', '*')]
        start_response('200 OK', headers)
        payload = self._format(items)
        logging.info("Sending %s" % payload)
        yield payload
        try:
            while True:
                item = queue.get(timeout=60)
                payload = self._format([item])
                logging.info("Sending %s" % payload)
                yield payload
        except (IOError, Empty) as exc:
            self.queue_lock.acquire()
            self.queues.remove(queue)
            self.queue_lock.release()
            logging.warn("Exception during request: %s" % exc)
        logging.info("Request completed")

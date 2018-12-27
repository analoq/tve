"""Domain module encompassess all domain logic"""
import threading
import time
from datetime import datetime, timedelta
import logging

class Domain(object):
    """Domain class for domain logic"""
    def __init__(self, persistence, acquisition, service):
        """Initializes Domain object"""
        self.persistence = persistence
        self.acquisition = acquisition
        self.service = service
        self.acquisition.set_callback(self._callback)
        self.thread = threading.Thread(target=self._thread)
        self.thread.start()

    def _callback(self, item):
        self.persistence.store(item['dt'],
                item['moisture'],
                item['luminence'],
                item['temperature'],
                item['humidity']
            )
        self.service.enqueue('recent', 'realtime', item)

    def _thread(self):
        while True:
            now = datetime.utcnow()
            now_floor = now.replace(minute=0,second=0,microsecond=0)
            next_time = now_floor + timedelta(hours=1)
            delta = (next_time - now).total_seconds()
            logging.info("Waiting for %d seconds to archive" % delta)
            time.sleep(delta)
            logging.info("Archiving")
            self.persistence.archive()
            items = self.persistence.historical_archive(hours=24)
            if items:
                self.service.enqueue('archive', 'preload', items)

    @staticmethod
    def round_hour(timestamp):
        f = timestamp.replace(minute=0, second=0, microsecond=0)
        c = f + timedelta(hours=1)
        if (timestamp - f) < (c - timestamp):
            return f
        else:
            return c

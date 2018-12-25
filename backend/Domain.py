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
        self.persistence.store(item['dt'], item['value'])
        self.service.enqueue('recent', 'realtime', item)

    def _thread(self):
        while True:
            now = datetime.utcnow()
            now_floor = now.replace(second=0,microsecond=0)
            next_time = now_floor + timedelta(minutes=15)
            time.sleep((next_time - now).total_seconds())
            logging.info("Archiving")
            items = self.persistence.archive()
            if items:
                self.service.enqueue('archive', 'realtime', items)

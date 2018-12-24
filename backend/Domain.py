"""Domain module encompassess all domain logic"""
import threading
import time
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
        self.service.enqueue(item)

    def _thread(self):
        while True:
            time.sleep(15*60)
            logging.info("Archiving")
            self.persistence.archive()

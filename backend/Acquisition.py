"""Data acquisition module"""
import time
import threading
import random
from datetime import datetime

class Acquisition(object):
    """Data acquisition class"""

    def __init__(self, callback):
        """Launch the acquisition thread and send samples to provided callback"""
        self.callback = callback
        # launch data acquisition thread
        self.thread = threading.Thread(target=self._thread)
        self.thread.daemon = True
        self.thread.start()

    def _thread(self):
        while True:
            item = {
                'dt': datetime.utcnow(),
                'value': random.randint(0, 1023),
            }
            self.callback(item)
            time.sleep(2)

"""Data acquisition module"""
import time
import threading
import random
from datetime import datetime

class Acquisition(object):
    """Data acquisition class"""

    def __init__(self):
        """Launch the acquisition thread"""
        self.callback = None
        # launch data acquisition thread
        self.thread = threading.Thread(target=self._thread)
        self.thread.daemon = True
        self.thread.start()

    def set_callback(self, callback):
        """Set callback to send samples to"""
        self.callback = callback

    def _thread(self):
        while True:
            item = {
                'dt': datetime.utcnow(),
                'value': random.randint(0, 1023),
            }
            if self.callback:
                self.callback(item)
            time.sleep(2)

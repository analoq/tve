"""Data acquisition module"""
import threading
import random
from datetime import datetime
import logging

import serial

class Acquisition(object):
    """Data acquisition class"""

    def __init__(self, path):
        """Launch the acquisition thread"""
        self.callback = None
        # open serial port
        self.ser = serial.Serial(path, timeout=60)
        # launch data acquisition thread
        self.thread = threading.Thread(target=self._thread)
        self.thread.daemon = True
        self.thread.start()

    def set_callback(self, callback):
        """Set callback to send samples to"""
        self.callback = callback

    def _thread(self):
        try:
            while True:
                line = self.ser.readline()
                if not line:
                    logging.warn('Serial port read timeout')
                    continue
                split = line.strip().split('\t')
                item = {
                    'dt': datetime.utcnow(),
                    'moisture': float(split[0]),
                    'luminence': float(split[1]),
                    'temperature': float(split[2]),
                    'humidity': float(split[3]),
                }
                if self.callback:
                    self.callback(item)
        except serial.serialutil.SerialException:
            logging.error('Serial port read failure!')

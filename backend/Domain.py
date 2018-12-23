"""Domain module encompassess all domain logic"""
from Persistence import Persistence
from Service import Service
from Acquisition import Acquisition


class Domain(object):
    """Domain class for domain logic"""
    def __init__(self):
        """Initializes Domain object"""
        self.persistence = Persistence('tve.db')
        self.acquisition = Acquisition(self._callback)
        self.service = Service(self.persistence)

    def _callback(self, item):
        self.persistence.store(item['dt'], item['value'])
        self.service.enqueue(item)

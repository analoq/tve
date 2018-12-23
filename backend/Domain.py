"""Domain module encompassess all domain logic"""

class Domain(object):
    """Domain class for domain logic"""
    def __init__(self, persistence, acquisition, service):
        """Initializes Domain object"""
        self.persistence = persistence
        self.acquisition = acquisition
        self.service = service
        self.acquisition.set_callback(self._callback)

    def _callback(self, item):
        self.persistence.store(item['dt'], item['value'])
        self.service.enqueue(item)

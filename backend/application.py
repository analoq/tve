"""Application launcher for use with uwsgi"""
import logging

import uwsgidecorators

from Persistence import Persistence
from Service import Service
from Acquisition import Acquisition
from Domain import Domain


@uwsgidecorators.postfork
def handler():
    """postfork hanlder, creates global domain object"""
    global domain
    persistence = Persistence('tve.db')
    acquisition = Acquisition('/dev/ttyACM0')
    service = Service(persistence)
    domain = Domain(persistence, acquisition, service)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    logging.info('Domain object initialized')


def application(environ, start_response):
    """web request handler, passes requests to domain handler"""
    global domain
    return domain.service.request(start_response)

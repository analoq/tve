"""Application launcher for use with uwsgi"""
import logging

import uwsgidecorators

from Domain import Domain


@uwsgidecorators.postfork
def handler():
    """postfork hanlder, creates global domain object"""
    global domain
    domain = Domain()
    logging.info('Domain object initialized')


def application(environ, start_response):
    """web request handler, passes requests to domain handler"""
    global domain
    return domain.service.request(start_response)

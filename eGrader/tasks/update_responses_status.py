import logging

from eGrader.core import db
from eGrader.models import Response


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def make_responses_inactive():
    make_inactive = db.session.query(Response).filter(
        Response.created_on == None).all()
    total = len(make_inactive)

    log.info('Total responses to make inactive: {0}'.format(total))

    count = 0
    for response in make_inactive:
        count += 1
        response.active = False
        db.session.add(response)
        log.info('Making response_id: {0} inactive'.format(response.id))
        log.info('Task completion: {0}'.format((float(count)/total) * 100))
    log.info('Saving updates to the database')
    db.session.commit()
    log.info('Make responses inactive task completed')


def make_responses_active():
    make_active = db.session.query(Response).filter(
        Response.created_on != None).all()
    total = len(make_active)

    log.info('Total responses to make active: {0}'.format(total))

    count = 0
    for response in make_active:
        count += 1
        response.active = True
        db.session.add(response)
        log.info('Making response_id: {0} active'.format(response.id))
        log.info('Task completion: {0}'.format((float(count)/total) * 100))
    log.info('Saving updates to the database')
    db.session.commit()
    log.info('Make responses active task completed')

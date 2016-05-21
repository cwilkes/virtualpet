import logging
import db
import models


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def record_event(event, context):
    logger.info('Event: %s' % (event, ))
    logger.info('Context: %s' % (context, ))
    user_id, pet_id, action = event['user'], event['pet'], event['action']
    db.add_event(user_id, pet_id, action)
    ret = models.events_to_json(db.get_events_for_user_and_pet(user_id, pet_id))
    logger.info('Ret for record_event: %s' % (ret, ))
    return ret

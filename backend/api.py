import logging
import db
import models
import urlparse


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def record_event_json_post(event, context):
    logger.info('Event1: %s' % (event, ))
    logger.info('Context1: %s' % (context, ))
    user_id, pet_id, action = event['user'], event['pet'], event['action']
    db.add_event(user_id, pet_id, action)
    ret = models.events_to_json(db.get_events_for_user_and_pet(user_id, pet_id))
    logger.info('Ret for record_event: %s' % (ret, ))
    return dict(user=user_id, pet_id=pet_id, actions=ret)


def _form_post_to_single_dict(post_string):
    ret = dict()
    for key, value in urlparse.parse_qs(post_string).items():
        ret[key] = value[0]
    return ret


def record_event(event, context):
    logger.info('Event2: %s' % (event, ))
    logger.info('Context2: %s' % (context, ))
    return record_event_json_post(_form_post_to_single_dict(event['body']), dict())

import boto3
from collections import defaultdict
from boto3.dynamodb.conditions import Key, Attr
import datetime
import models
import json


SNS_TOPIC_ADD_EVENT = 'arn:aws:sns:us-east-1:052602034920:vp_added_animal_event'

dynamodb = boto3.resource('dynamodb')
tbl_animal_events = dynamodb.Table('vp_animal_events')
sns_animal_events = boto3.resource('sns').Topic(SNS_TOPIC_ADD_EVENT)


def _mk_dict_with_set(items, key_name, value_name):
    ret = defaultdict(set)
    for item in items:
        ret[item[key_name]].add(item[value_name])
    return ret


def get_users_and_pets():
    res = tbl_animal_events.scan(FilterExpression=Attr('event_seq').eq(0))
    return _mk_dict_with_set(res['Items'], 'user_id', 'pet_id')


def _mk_key(user_id, pet_id):
    return '%s_%s' % (user_id, pet_id)


def _get_event_ids(user_id, pet_id):
    res = tbl_animal_events.query(KeyConditionExpression=Key('user_pet_id').eq(_mk_key(user_id, pet_id)))
    return sorted([_['event_seq'] for _ in res['Items']])


def add_event(user_id, pet_id, action):
    current_event_ids = _get_event_ids(user_id, pet_id)
    next_event_id = current_event_ids[-1] + 1 if current_event_ids else 0
    item = dict(
        user_id=user_id,
        pet_id=pet_id,
        user_pet_id=_mk_key(user_id, pet_id),
        event_seq=next_event_id,
        action=action,
        date=datetime.datetime.now().isoformat()
    )
    tbl_animal_events.put_item(Item=item)
    # this should be done in a trigger on the table but can't figure it out
    events = get_events_for_user_and_pet(user_id, pet_id)
    ret = dict(user=user_id, pet=pet_id, events=models.events_to_json(events))
    sns_message(json.dumps(ret))
    return ret


def sns_message(msg):
    sns_animal_events.publish(Message=msg)


def get_events_for_user_and_pet(user_id, pet_id):
    res = tbl_animal_events.query(KeyConditionExpression=Key('user_pet_id').eq(_mk_key(user_id, pet_id)))
    return models.mk_pet_events(res['Items'])

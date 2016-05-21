from collections import namedtuple
import dateutil.parser
import json


PetEvent = namedtuple('PetEvent', 'action date')


def mk_pet_events(items):
    return [PetEvent(_['action'], dateutil.parser.parse(_['date'])) for _ in items]


def events_to_json(events):
    return [dict(action=_.action, date=_.date.isoformat()) for _ in events]


def events_to_json_str(events):
    return json.dumps(events_to_json(events))


def events_json_str_to_pet_events(event_str):
    return mk_pet_events(json.loads(event_str))


def parse_sns_notice(sns_notice):
    return events_json_str_to_pet_events(sns_notice['Message'])

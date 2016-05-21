from __future__ import print_function

import boto3
import json
import logging

from base64 import b64decode
from urllib2 import Request, urlopen, URLError, HTTPError


ENCRYPTED_HOOK_URL = 'CiB64HxuzoF4M42YvDiL+YmWvePope+3WZ/mEQq1dDR3OhLQAQEBAgB4euB8bs6BeDONmLw4i/mJlr3j6KXvt1mf5hEKtXQ0dzoAAACnMIGkBgkqhkiG9w0BBwaggZYwgZMCAQAwgY0GCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMUw9QePxorFaTsSt/AgEQgGCYzNh6rMe0+/u0AzDkJP2qtVp0JvoO0lqJPU2hUpiDYYtNMU6Y8BSzYP/C3beA5dXwNLoTekjUvPspnxR7vOw5+/us3Fw6RUZ6HIFBN//pp3iINB7e+BOf+pMvrC4whrY='
SLACK_CHANNEL = 'virtualpet'  # Enter the Slack channel to send a message to

HOOK_URL = "https://" + boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED_HOOK_URL))['Plaintext']

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Event: " + str(event))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info("Message: " + str(message))

    user, pet, events = message['user'], message['pet'], message['events']

    slack_message = {
        'channel': SLACK_CHANNEL,
        'text': '%s just %s %s' % (user, events[-1]['action'], pet)
    }

    req = Request(HOOK_URL, json.dumps(slack_message))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)

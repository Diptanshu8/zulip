# Webhooks for external integrations.
from __future__ import absolute_import
from django.utils.translation import ugettext as _
from zerver.lib.actions import check_send_message
from zerver.lib.response import json_success, json_error
from zerver.decorator import REQ, has_request_variables, api_key_only_webhook_view
from zerver.lib.validator import check_dict, check_string
from zerver.models import Client, UserProfile

from django.http import HttpRequest, HttpResponse
from six import text_type
from typing import Dict, Any, Iterable, Optional

import datetime
@api_key_only_webhook_view('Beeminder')
@has_request_variables
def api_beeminder_webhook(request, user_profile, client,
                           payload=REQ(argument_type='body'), stream=REQ(default='test'),
                           topic=REQ(default='Beeminder bot')):
    # type: (HttpRequest, UserProfile, Client, Dict[str, Iterable[Dict[str, Any]]], text_type, Optional[text_type]) -> HttpResponse

    # construct the body of the message
    body = 'Hello! I am the Beeminder bot! :smile:'

    # try to add the Wikipedia article of the day
    # return appropriate error if not successful
    try:
        body_template = '\nYou are derailing from the goal **{goal[title]}**, pledge of **{goal[pledge]}** will forefeit upon derailing. To counter derailing, you need **{goal[limsum]}**'
        body += body_template.format(**payload)
    except KeyError as e:
        return json_error(_("Missing key {} in JSON").format(str(e)))

    # send the message
    check_send_message(user_profile, client, 'private', ['cordelia@zulip.com'], topic, body)
    #check_send_message(user_profile, client, 'stream', [stream], topic, body)
    
    return json_success()

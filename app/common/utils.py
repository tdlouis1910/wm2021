import decimal
from datetime import timezone, datetime, timedelta
from functools import wraps, partial

from werkzeug.exceptions import abort
from app.common import messages

import boto3
import jwt
import requests
from flask import current_app, g, request, jsonify, json

from app.common.constants import RESPONSE
from app.common.extensions import db
from app.common.messages import MESSAGES

from models import User


# from app.common.extensions import mail


# from flask_mail import Message
# from app.models import *

# def send_push(to, title, message, url=None):
#     data = {
#         'priority': 'high',
#         'notification': {
#             'title': title,
#             'body': message,
#             'sound': 'default',
#             'icon': 'push_icon',
#             'android_channel_id': 'noni_high'
#         },
#         'data': {
#             'click_action': 'FLUTTER_NOTIFICATION_CLICK'
#         }
#     }

#     if url is not None:
#         data['data']['url'] = url

#     if not isinstance(to, list):
#         data['to'] = to.strip()

#         r = requests.post(current_app.config['FCM_API_URL'], data=json.dumps(data), headers={
#             'Authorization': 'key=' + current_app.config['FCM_AUTH_KEY'],
#             'Content-Type': 'application/json'
#         })

#         result = r.json()
#     else:
#         result = []
#         for i in range(0, len(to), 500):
#             data['registration_ids'] = to[i:i+500]

#             r = requests.post(current_app.config['FCM_API_URL'], data=json.dumps(data), headers={
#                 'Authorization': 'key=' + current_app.config['FCM_AUTH_KEY'],
#                 'Content-Type': 'application/json'
#             })

#             result.append(r.json())

#     # TODO: 푸시 발송 기록

#     return result


def datetime_format(dt, f):
    return dt.strftime(f) if dt else None


# def datetime_local(dt, f):
#     offset = g.utc_offset if hasattr(g, 'utc_offset') else -time.timezone / 60
#     return datetime_format(dt.replace(tzinfo=timezone.utc).astimezone(tz=timezone(timedelta(seconds=offset * 60))), f)


# def datetime_utc(dt):
#     offset = g.utc_offset if hasattr(g, 'utc_offset') else -time.timezone / 60

#     if type(dt) == datetime:
#         return dt.replace(tzinfo=timezone(timedelta(seconds=offset * 60))).astimezone(tz=timezone.utc)
#     else:
#         return dt


def generate_token(payload):
    return jwt.encode(payload, current_app.config['SECRET_KEY']).decode('UTF-8')


def validate_token(token):
    try:
        return jwt.decode(token, current_app.config['SECRET_KEY'])
    except jwt.exceptions.PyJWTError:
        return None


def parse_token():
    auth_header = request.headers.get('Authorization', '').split()
    if len(auth_header) == 2:
        token = auth_header[1]
    else:
        token = request.args.get('token')

    try:
        return validate_token(token)
    except jwt.exceptions.PyJWTError:
        return None


def formvalidation(data, validation_form):
    for key in validation_form:
        value = data.get(key, None)
        if value is None or (isinstance(value, str) and value.strip() == ''):
            return getresponse('VALIDATION_ERROR')

    return getresponse('SUCCESS')



def getparams():
    if request.get_json():
        return request.get_json()
    if request.form:
        return request.form

    return request.args


def getmessage(message):
    
    return MESSAGES['RESPONSE'][message]
    # for m in message:
    #     if m not in locale:
    #         break
    #     else:
    #         locale = locale[m]

    # return locale if type(locale) is str else ''


def getresponse(result, message=None):
    if result in RESPONSE:
        res = RESPONSE[result].copy()
        if message is None:
            res['message'] = getmessage(result)
            return res
        else:
            res['message'] = message
            return res

    return None


def authentication(only, bypass=False):
    def _authentication(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            from models import User

            member = None
            token_type = None

            try: 
                token = parse_token()

                if token:
                    token_type = token.get('type', '')

                    if token_type in only:
                        if token_type == 'user':
                            member = User.query.get(token.get('idx', ''))

                            if member and (member.deleted_at is not None):
                                member = None

                if member:
                    kwargs.update({
                        'auth': {
                            'token': token,
                            'type': token_type,
                            'member': member
                        }
                    })
                    auth = {
                        'type': token_type,
                        'idx': member.idx,
                    }

                    if token_type == 'user':
                        auth['email'] = member.email
                    

                    return f(*args, **kwargs)
                elif bypass:
                        kwargs.update({
                            'auth': None
                        })
                        return f(*args, **kwargs)

                return jsonify(getresponse('UNAUTHENTICATED')), 401
            except: abort(500)
        return decorator
    return _authentication


def alchemyencoder(obj):
    import datetime

    if isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')












from dataclasses import dataclass
import json

from flask import current_app, request
from flask_marshmallow import fields
import pytz

from webapp.model import ma


@dataclass
class TaskInfo:
    task_id: str
    bp_id: str
    bp_type: str
    bp_title: str
    bp_description: str
    user: str


def parse_post_data(raw_data):
    data_decode = raw_data.decode('utf8')

    try:
        data_json = json.loads(data_decode)
    except json.JSONDecodeError:
        return None

    if not data_json or 'task_id' not in data_json:
        return None

    return TaskInfo(**data_json)


def api_key_is_correct():
    client_api_key = request.args.get('api_key')
    if client_api_key != current_app.config['API_KEY']:
        return False
    return True


def convert_to_vl_time(time_in_utc):
    tz_utc = pytz.utc
    tz_vl = pytz.timezone('Asia/Vladivostok')
    return tz_utc.localize(time_in_utc, is_dst=None) \
        .astimezone(tz_vl)


class TaskSchema(ma.Schema):
    verdict_date = fields.fields.DateTime('%Y%m%d%H%M%S')

    class Meta:
        fields = ('task_id',
                  'bp_id',
                  'user_id',
                  'verdict',
                  'message',
                  'verdict_date'
                  )


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

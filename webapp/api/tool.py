from dataclasses import dataclass
import json

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


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('task_id', 'bp_id',
                  'user_id', 'verdict',
                  'message', 'verdict_date'
                  )


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

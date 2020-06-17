from dataclasses import dataclass
import json


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

    if not data_json or not 'task_id' in data_json:
        return None

    return TaskInfo(**data_json)
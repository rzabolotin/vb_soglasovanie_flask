from flask import (Blueprint, abort, current_app, jsonify, make_response,
                   request)

from webapp.api.tools import (api_key_is_correct, convert_to_vl_time,
                              load_file_attachment, load_task, parse_post_data,
                              task_schema, tasks_schema)
from webapp.model import db
from webapp.soglasovanie.models import (BusinessProcess, FileAttachment,
                                        SoglasovanieTask)

blueprint = Blueprint("api", __name__, url_prefix="/api")


@blueprint.route("/get_task/<string:task_id>", methods=["GET"])
def get_task(task_id: str):
    """Выдать описание задачи в формате json"""

    if not api_key_is_correct():
        abort(403)

    task = SoglasovanieTask.query.get(task_id)
    if not task:
        return abort(404)

    task.verdict_date = convert_to_vl_time(task.verdict_date)

    return task_schema.jsonify(task)


@blueprint.route("/get_tasks", methods=["GET"])
def get_tasks():
    """
    Выдать список всех задач в формте json
    время выдается в тайм-зоне Владивостока
    """
    if not api_key_is_correct():
        abort(403)

    tasks = SoglasovanieTask.query.all()

    for task in tasks:
        task.verdict_date = convert_to_vl_time(task.verdict_date)

    return tasks_schema.dumps(tasks)


@blueprint.route("/post_task", methods=["POST"])
def post_task():
    """Загрузить новую задачу (и связанную информацию тоже) на сервер"""
    if not api_key_is_correct():
        abort(403)

    task_info = parse_post_data(request.data)
    if not task_info:
        return abort(400)

    task = load_task(task_info)

    return task_schema.jsonify(task)


@blueprint.route("/post_file", methods=["POST"])
def post_file():
    """Загрузить файл к бизнес-процессу"""

    if not api_key_is_correct():
        abort(403)

    posted_data = request.form["fileinfo"]
    posted_file = request.files["datafile"].read()

    file_info = parse_post_data(posted_data, "file")
    if not file_info:
        return abort(400)

    file = load_file_attachment(file_info, posted_file)
    if file:
        return "Файл добавлен на сервер"
    else:
        abort(404)


@blueprint.errorhandler(400)
def not_found(error):
    return make_response(jsonify({"error": "bad request"}), 400)


@blueprint.errorhandler(403)
def not_found(error):
    return make_response(jsonify({"error": "please, enter correct api key"}), 403)


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "not found"}), 404)

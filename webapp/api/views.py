from flask import abort, Blueprint, jsonify, make_response, request

from webapp.model import db
from webapp.soglasovanie.models import SoglasovanieTask, BusinessProcess
from webapp.user.models import User
from webapp.api.tool import api_key_is_correct, convert_to_vl_time,\
    parse_post_data, task_schema, tasks_schema


blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/get_task/<string:task_id>', methods=['GET'])
def get_task(task_id:str):

    if not api_key_is_correct():
        abort(403)

    task = SoglasovanieTask.query.get(task_id)
    if not task:
        return abort(404)

    task.verdict_date = convert_to_vl_time(task.verdict_date)

    return task_schema.jsonify(task)


@blueprint.route('/get_tasks', methods=['GET'])
def get_tasks():

    if not api_key_is_correct():
        abort(403)

    tasks = SoglasovanieTask.query.all()

    for task in tasks:
        task.verdict_date = convert_to_vl_time(task.verdict_date)

    return tasks_schema.dumps(tasks)


@blueprint.route('/post_task', methods=['POST'])
def post_task():

    if not api_key_is_correct():
        abort(403)

    task_info = parse_post_data(request.data)
    if not task_info:
        return abort(400)

    user = User.query.filter(User.user_name == task_info.user).first()
    if not user:
        user = User(user_name=task_info.user)
        db.session.add(user)

    bp = BusinessProcess.query.filter(BusinessProcess.bp_id == task_info.bp_id).first()
    if bp:
        bp.title = task_info.bp_title
        bp.description = task_info.bp_description
    else:
        bp = BusinessProcess(
            bp_id=task_info.bp_id,
            bp_type=task_info.bp_type,
            title=task_info.bp_title,
            description=task_info.bp_description
        )
    db.session.add(bp)

    task = SoglasovanieTask.query.filter(SoglasovanieTask.task_id == task_info.task_id).first()
    if not task:
        task = SoglasovanieTask(
            task_id=task_info.task_id,
            bp_id=bp.bp_id,
            user_id=user.id,
        )

    db.session.add(task)
    db.session.commit()

    return task_schema.jsonify(task)


@blueprint.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error':'bad request'}), 400)


@blueprint.errorhandler(403)
def not_found(error):
    return make_response(jsonify({'error':'please, enter correct api key'}), 403)


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'not found'}), 404)

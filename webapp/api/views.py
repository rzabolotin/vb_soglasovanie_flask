import json

from flask import abort, Blueprint, current_app, jsonify, make_response, request

from webapp.model import db
from webapp.soglasovanie.models import SoglasovanieTask, BusinessProcess
from webapp.user.models import User
from webapp.api.tool import parse_post_data

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/get_task/<string:task_id>', methods=['GET'])
def get_task(task_id:str):
    
    task = SoglasovanieTask.query.filter(SoglasovanieTask.task_id == task_id).first()
    if not task:
        return abort(404)
    
    return jsonify(task.api_repr())


@blueprint.route('/post_task', methods=['POST'])
def post_task():
    """
     sample_input = {
        'task_id': '000000123',
        'bp_id': 'ВБ0000011',
        'bp_type': 'ТД_ЗаявкаНаОплату',
        'bp_title': 'Заявка на оплату Заболотин 100000рублей, услуги по 1С',
        'bp_decription': 'Заявка на оплату ... Контрагент: Заболотин ... Назначение платежа ...',
        'user': 'Перехожук'
    }

    data_decode = request.data.decode('utf8')
    try:
        data_json = json.loads(data_decode)
    except json.JSONDecodeError:
        return abort(400)

    if not data_json or not 'task_id' in data_json:
        return abort(400)
    """

    task_info = parse_post_data(request.data)
    if not task_info:
        return abort(400)

    task = SoglasovanieTask.query.filter(SoglasovanieTask.task_id == task_info.task_id).first()
    if task:
        return abort(400)

    user = User.query.filter(User.username == task_info.user).first()
    if not user:
        user = User(username=task_info.user)
        db.session.add(user)

    bp = BusinessProcess.query.filter(BusinessProcess.bp_id == task_info.bp_id).first()

    if not bp:
        bp = BusinessProcess(
            bp_id=task_info.bp_id,
            bp_type=task_info.bp_type,
            title=task_info.bp_title,
            description=task_info.bp_description
        )
        db.session.add(bp)

    task = SoglasovanieTask(
        task_id=task_info.task_id,
        bp_id=bp.bp_id,
        user_id=user.id,
    ) 

    db.session.add(task)
    db.session.commit()

    return jsonify(task.api_repr())


@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'not found'}), 404)

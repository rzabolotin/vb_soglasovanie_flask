import json

from flask import abort, Blueprint, current_app, jsonify, make_response, request
from flask_login import current_user, login_required
from sqlalchemy.ext.declarative import DeclarativeMeta

from webapp.model import db
from webapp.soglasovanie.models import SoglasovanieTask, BusinessProcess
from webapp.user.models import User


blueprint = Blueprint('api', __name__, url_prefix='/api')

@blueprint.route('/get_task/<string:task_id>', methods=['GET'])
def get_task(task_id:str):
    
    task = SoglasovanieTask.query.filter(SoglasovanieTask.task_id == task_id).first()
    if not task:
        return abort(404)
    
    return jsonify(task.api_repr())

@blueprint.route('/post_task', methods=['POST'])
def post_task():
       
    data_decode = request.data.decode('utf8')

    data_json = json.loads(data_decode)

    current_app.logger.info(data_json)

    return data_json
    
    
    """
    
    if not request.json or not 'task_id' in request.json:
        abort(400)
    
    sample_data = {
        'task_id': '000000123',
        'bp_id': 'ВБ0000011',
        'bp_type': 'ТД_ЗаявкаНаОплату',
        'bp_title': 'Заявка на оплату Заболотин 100000рублей, услуги по 1С',
        'bp_decription': 'Заявка на оплату ... Контрагент: Заболотин ... Назначение платежа ...',
        'user': 'Перехожук'
    }

    task = SoglasovanieTask.query.filter(SoglasovanieTask.task_id == request.json.task_id)
    
    if task:
        abort(400)

    user = User.query.filter(User.username == request.json.user).first()

    if not user:
        user = User(username=request.json.user)
        db.session.add(user)

    bp = BusinessProcess.query.filter(BusinessProcess.bp_id == request.json.bp_id).first()

    if not bp:
        bp = BusinessProcess(
            bp_id = request.json.bp_id,
            bp_type = request.json.bp_type,
            title = request.json.bp_title,
            description = request.json.bp_description
        )
        db.session.add(bp)

    task = SoglasovanieTask(
        task_id = request.json.task_id,
        bp_id = bp.bp_id,
        user_id = user.id,
    ) 

    db.session.add(task)
    db.session.commit()

    return jsonify(task.api_repr())

@blueprint.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'not found'}), 404)
"""
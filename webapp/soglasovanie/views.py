from datetime import datetime
import json

from flask import abort, Blueprint, flash, current_app, render_template, redirect, request, send_file, url_for
from flask_login import current_user, login_required

from webapp.model import db
from webapp.soglasovanie.forms import TaskForm
from webapp.soglasovanie.models import SoglasovanieTask, FileAttachment

blueprint = Blueprint('soglasovanie', __name__, url_prefix='/')


@blueprint.route('/')
@blueprint.route('/<string:task_filter>')
@login_required
def index(task_filter: str = None):
    """
    Список задач текущего пользователя
    Варианты фильтра:
    active - не выполненные
    closed - выполненные
    all(default) - все задачи
    """
    user_tasks = SoglasovanieTask.query.filter(SoglasovanieTask.user_id == current_user.id)

    if task_filter == 'active':
        list_of_tasks = user_tasks.filter(SoglasovanieTask.verdict == None).all()
    elif task_filter == 'closed':
        list_of_tasks = user_tasks.filter(SoglasovanieTask.verdict != None).all()
    else:
        list_of_tasks = user_tasks.all()
    page_title = 'Все согласования'

    return render_template('soglasovanie/list.html',
                           page_title=page_title,
                           task_filter=task_filter,
                           list_of_tasks=list_of_tasks
                           )


@login_required
@blueprint.route('/show_task/<string:task_id>')
def show_task(task_id: str):
    """Показать страницу задачи"""

    task = SoglasovanieTask.query.filter(SoglasovanieTask.task_id == task_id).first()
    if not task:
        abort(404)

    page_title = task.bp.title
    bp_info = json.loads(task.bp.description)
    bp_files = task.bp.files

    form = TaskForm(task_id=task_id, bp_type=task.bp.bp_type)
    form.verdict = task.verdict
    form.message = task.message

    verdict_from_params = request.args.get('verdict')
    if verdict_from_params:
        form.verdict = verdict_from_params

    return render_template('soglasovanie/task.html',
                           page_title=page_title,
                           task=task,
                           bp_info=bp_info,
                           bp_files=bp_files,
                           form=form
                           )


@login_required
@blueprint.route('/perform_task', methods=['POST'])
def perform_task():
    """
    Обработка формы из задачи
    Задача может быть выполнена или отклонена
    """

    task_form = TaskForm()

    task = SoglasovanieTask.query.filter(SoglasovanieTask.task_id == task_form.task_id.data).first()
    if task.verdict:
        return redirect(url_for('soglasovanie.index', task_filter='active'))

    if task_form.validate_on_submit():

        task.verdict = task_form.verdict.data
        task.verdict_date = datetime.utcnow()
        task.message = task_form.message.data
        db.session.commit()

        flash('Задача выполнена')
        return redirect(url_for('soglasovanie.index', task_filter='active'))

    else:
        for field, errors in task_form.errors.items():
            for error in errors:
                flash(error)
        return redirect(url_for('soglasovanie.show_task',
                                task_id=task_form.task_id.data,
                                verdict=task_form.verdict.data
                                )
                        )


@login_required
@blueprint.route('/get_file/<int:file_id>', methods=['GET'])
def get_file(file_id: int):
    """Выдать файл по его номеру в базе"""

    file = FileAttachment.query.get(file_id)
    if not file:
        abort(404)

    return send_file(file.get_file_path(),
                     attachment_filename=file.filename,
                     as_attachment=True
                     )

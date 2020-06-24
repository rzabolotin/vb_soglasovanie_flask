from datetime import datetime

from flask import abort, Blueprint, flash, current_app, render_template, redirect, request, url_for
from flask_login import current_user, login_required

from webapp.model import db
from webapp.soglasovanie.forms import TaskForm
from webapp.soglasovanie.models import SoglasovanieTask

blueprint = Blueprint('soglasovanie', __name__, url_prefix='/')


@blueprint.route('/')
@blueprint.route('/<string:task_filter>')
@login_required
def index(task_filter: str = None):
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
    task = SoglasovanieTask.query.filter(SoglasovanieTask.task_id == task_id).first()
    if not task:
        abort(404)

    page_title = task.bp.title
    form = TaskForm(task_id=task_id, bp_type=task.bp.bp_type)

    form.verdict = task.verdict
    form.message = task.message

    verdict_from_params = request.args.get('verdict')
    if verdict_from_params:
        form.verdict = verdict_from_params

    return render_template('soglasovanie/task.html',
                           page_title=page_title,
                           task=task,
                           form=form
                           )


@login_required
@blueprint.route('/perform_task', methods=['POST'])
def perform_task():
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

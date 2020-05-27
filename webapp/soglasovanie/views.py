from datetime import datetime

from flask import abort,Blueprint, flash, current_app, render_template, redirect, request, url_for
from flask_login import current_user, login_required

from webapp.model import db
from webapp.soglasovanie.forms import TaskForm
from webapp.soglasovanie.models import SoglasovanieTask

blueprint = Blueprint('soglasovanie', __name__, url_prefix='/')

@blueprint.route('/')
def index():
    
    page_title = 'Все согласования'
    list_of_tasks = SoglasovanieTask.query.all()
    return render_template('soglasovanie/list.html', 
        page_title=page_title,  
        list_of_tasks=list_of_tasks
        )


@blueprint.route('/show_task/<string:task_id>')
def show_task(task_id:str):
    
    task = SoglasovanieTask.query.filter(SoglasovanieTask.task_id == task_id).first()
    if not task:
        abort(404)

    page_title = task.bp.title
    form = TaskForm(task_id=task_id, bp_type = task.bp.bp_type)
    return render_template('soglasovanie/task.html',
        page_title = page_title,
        task = task,
        form = form
        )

@blueprint.route('/perform_task', methods=['POST'])
def perform_task():
    taskForm = TaskForm()
    if taskForm.validate_on_submit():
        
        task = SoglasovanieTask.query.filter(SoglasovanieTask.task_id == taskForm.task_id.data).first()
        task.verdict = taskForm.verdict.data
        task.verdict_date = datetime.now()
        task.message = taskForm.message.data
        db.session.commit()

        flash('Задача выполнена')
        return redirect(url_for('soglasovanie.index'))

    else:
        for field, errors in taskForm.errors.items():
            for error in errors:
                flash(error)
        return redirect(url_for('soglasovanie.show_task', task_id=taskForm.task_id.data))


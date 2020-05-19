from flask import abort,Blueprint, flash, current_app, render_template, redirect, request
from flask_login import current_user, login_required

from webapp.model import db
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
    return render_template('soglasovanie/task.html',
        page_title = page_title,
        task = task
        )

@blueprint.route('/perform_task', methods=['POST'])
def perform_task():
    page_title = f'Задача'
    return render_template('soglasovanie/task.html',
        page_title = page_title,
        task = {}
        )


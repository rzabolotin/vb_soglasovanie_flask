from flask import abort,Blueprint, flash, current_app, render_template, redirect, request
from flask_login import current_user, login_required

from webapp.model import db
from webapp.soglasovanie.models import SoglasovanieTask

blueprint = Blueprint('soglasovanie', __name__, url_prefix='/')

@blueprint.route('/')
def index():
    
    page_title = 'Все согласования'
    list_of_tasks = SoglasovanieTask.query.all()
    return render_template('soglasovanie/soglasovanie_all.html', 
        page_title=page_title,  
        list_of_tasks=list_of_tasks
        )
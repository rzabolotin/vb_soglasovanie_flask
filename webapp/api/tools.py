import json
from dataclasses import dataclass
from datetime import datetime
from typing import BinaryIO
import logging

import pytz
from flask import current_app, request
from flask_marshmallow.fields import fields

from webapp.model import db, ma
from webapp.soglasovanie.models import BusinessProcess, FileAttachment, SoglasovanieTask
from webapp.user.models import User


@dataclass
class TaskInfo:
    task_id: str
    bp_id: str
    bp_type: str
    bp_title: str
    bp_date: str
    bp_description: str
    user: str
    verdict: str
    message: str


@dataclass
class FileInfo:
    bp_id: str
    file_type: str
    filename: str
    file_ext: str


def parse_post_data(raw_data, data_type="task"):
    """
    Разбирает дату полученную из POST
    raw_data может быть строкой или строкой байт
    внутри должен быть json
    внутри json может быть 2 формата (task и file)
    Возвращаем соответственно TaskInfo или FileInfo
    """

    if type(raw_data) == str:
        data_decode = raw_data
    else:
        data_decode = raw_data.decode("utf8")

    try:
        data_json = json.loads(data_decode)
    except json.JSONDecodeError:
        return None

    if data_type == "task":
        if not data_json or "task_id" not in data_json:
            return None
        task_info = TaskInfo(**data_json)
        if task_info.verdict == "":
            task_info.verdict = None
        return task_info

    elif data_type == "file":
        if not data_json or "filename" not in data_json:
            return None

        file_info = FileInfo(**data_json)
        return file_info

    else:
        return None


def parse_date_from_string_and_convert_to_utc(date_string: str):
    """
    Эта функция приниммет дату, поулченную по АПИ (в формате 1с, в Владивостокском часовой пояс, и приводить ее к utc
    """
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    tz_utc = pytz.utc
    tz_vl = pytz.timezone("Asia/Vladivostok")

    value = datetime.strptime(date_string, DATE_FORMAT)

    value = tz_vl.localize(value, is_dst=None)
    return value.astimezone(tz_utc)


def load_task(task_info: TaskInfo):
    """
    Загружает задачу и связанную информацию (User и BusinessProcess) в базу
    Возвращает задачу
    """

    user = User.query.filter(User.user_name == task_info.user.lower()).first()
    if not user:
        user = User(user_name=task_info.user.lower(), full_user_name=task_info.user)
        user.set_password(current_app.config["DEFAULT_PASS"])
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
            description=task_info.bp_description,
        )
    if not bp.date:
        bp.date = parse_date_from_string_and_convert_to_utc(task_info.bp_date)

    db.session.add(bp)

    logging.info("loading task")

    task = SoglasovanieTask.query.filter(SoglasovanieTask.task_id == task_info.task_id).first()
    if task:
        logging.info(f"updating task. new user id {user.id}")
        task.user_id = user.id
        if not task.verdict:
            task.verdict = task_info.verdict
            task.message = task_info.message
    else:
        task = SoglasovanieTask(
            task_id=task_info.task_id,
            bp_id=bp.bp_id,
            user_id=user.id,
            verdict=task_info.verdict,
            message=task_info.message,
        )

    db.session.add(task)
    db.session.commit()

    return task


def load_file_attachment(file_info: FileInfo, posted_file: BinaryIO):
    """
    Загружаем файл, связанный с бизнес процессом
    Если бизнес процесса нету - то не загружаем
    """

    bp = BusinessProcess.query.filter(BusinessProcess.bp_id == file_info.bp_id).first()
    if not bp:
        return None

    file = FileAttachment.query.filter(
        (FileAttachment.bp_id == file_info.bp_id) & (FileAttachment.filename == file_info.filename)
    ).first()
    if not file:
        file = FileAttachment(
            bp_id=file_info.bp_id,
            filename=file_info.filename,
            file_type=file_info.file_type,
            file_ext=file_info.file_ext,
        )
        db.session.add(file)
        db.session.commit()

    file.save_file(posted_file)

    return file


def api_key_is_correct():
    """Проверяет что есть параметры api_key и что он равен ключу, заданному в settings"""

    client_api_key = request.args.get("api_key")
    if client_api_key != current_app.config["API_KEY"]:
        return False
    return True


def convert_to_vl_time(time_in_utc):
    """Переводит дату в UTC в локальное время во Владивостоке"""

    if not time_in_utc:
        return time_in_utc

    tz_utc = pytz.utc
    tz_vl = pytz.timezone("Asia/Vladivostok")
    return tz_utc.localize(time_in_utc, is_dst=None).astimezone(tz_vl)


class UserSchema(ma.Schema):
    """Конвертер marshmallow для User"""

    class Meta:
        fields = (
            "id",
            "user_name",
        )


class TaskSchema(ma.Schema):
    """Конвертер marshmallow для SoglasovanieTask"""

    verdict_date = fields.DateTime("%Y%m%d%H%M%S")
    user = fields.Nested(UserSchema)

    class Meta:
        fields = ("task_id", "bp_id", "user", "verdict", "message", "verdict_date")


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

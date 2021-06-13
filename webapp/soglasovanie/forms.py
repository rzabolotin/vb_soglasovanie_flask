from flask_wtf import FlaskForm
from wtforms import HiddenField, RadioField, StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class TaskForm(FlaskForm):
    task_id = HiddenField("ИД заявки", validators=[DataRequired()])
    bp_type = HiddenField("Вид бизнес процесса", validators=[DataRequired()])
    verdict = RadioField(
        "Решение",
        choices=[("success", "Утвердить"), ("mistake", "Отправить замечание")],
        render_kw={"class": "d-none"},
    )
    message = StringField("Замечание")
    submit = SubmitField("Отправить", render_kw={"class": "btn btn-primary"})

    def validate_message(self, message):
        if self.verdict.data == "mistake" and not self.message.data:
            raise ValidationError("Необходимо указать замечание!")

from pathlib import Path

from flask import current_app
from sqlalchemy.orm import relationship

from webapp.model import db


class BusinessProcess(db.Model):
    bp_id = db.Column(db.String(20), primary_key=True, autoincrement=False, )
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    bp_type = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Business Process #{}:  {}>'.format(self.bp_id, self.title)


class SoglasovanieTask(db.Model):
    task_id = db.Column(db.String(20), primary_key=True, autoincrement=False)
    bp_id = db.Column(db.String(20), db.ForeignKey('business_process.bp_id'), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    verdict = db.Column(db.String)
    message = db.Column(db.String)
    verdict_date = db.Column(db.DateTime)

    bp = relationship('BusinessProcess', backref='tasks')
    user = relationship('User', backref='tasks')

    def __repr__(self):
        return '<Soglasovanie task {} {}>'.format(self.task_id, self.user_id)


class FileAttachment(db.Model):
    file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String, nullable=False)
    bp_id = db.Column(db.String(20), db.ForeignKey('business_process.bp_id'), index=True, nullable=False)
    file_type = db.Column(db.String(20))

    bp = relationship('BusinessProcess', backref='files')

    def __repr__(self):
        return '<File {}>'.format(self.filename)

    def save_file(self, file_raw_data):
        base_dir = Path(current_app.config['BP_ATTACHMENT_DIR'])
        bp_dir = base_dir / self.bp_id
        bp_dir.mkdir(parents=True, exist_ok=True)
        file_path = bp_dir / self.filename
        with open(file_path, 'w') as f:
            f.write(file_raw_data)


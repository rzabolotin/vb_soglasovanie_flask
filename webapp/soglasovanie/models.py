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
    verdict_send_to_1c = db.Column(db.Boolean)

    bp = relationship('BusinessProcess', backref='tasks')
    user = relationship('User', backref='tasks')

    def __repr__(self):
        return '<Soglasovanie task {} {}>'.format(self.task_id, self.user_id)

    def api_repr(self):
        return {
            'task_id': self.task_id,
            'bp_id': self.bp_id,
            'user': self.user.username,
            'verdict': self.verdict,
            'message': self.message,
            'verdict_date': self.verdict_date
        }

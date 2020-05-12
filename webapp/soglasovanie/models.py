from webapp.model import db

class SoglasovanieTask(db.Model):
    id = db.Column(db.String, primary_key=True)
    bp_id = db.Column(db.String, nullable=False)
    bp_description = db.Column(db.String, nullable=False)
    bp_type = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String)
    message = db.Column(db.String)
    date_of_action = db.Column(db.DateTime)
    
    def __repr__(self):
        return '<Soglasovanie task {} {}>'.format(self.id, self.description)




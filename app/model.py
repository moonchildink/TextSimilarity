from . import db
import datetime
from flask import jsonify


class Docx(db.Model):
    __tablename__ = 'docx'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), unique=True)
    upload_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    timestamp = db.Column(db.String(16), nullable=False)
    client_ip = db.Column(db.String(32), nullable=False)
    author = db.Column(db.String(32), nullable=True)
    created = db.Column(db.DateTime, nullable=True)
    modified = db.Column(db.DateTime, nullable=True)
    last_saved_by = db.Column(db.String(32), nullable=True)
    save_path = db.Column(db.String(192), unique=True, nullable=False)

    def to_json(self):
        return jsonify({
            'id': self.id,
            'filename': self.filename,
            'upload_time': self.upload_time,
            'time_stamp': self.timestamp,
            'client_ip': self.client_ip,
            'author': self.author,
            'created': self.created,
            'modified': self.modified,
            'last_saved_by': self.last_saved_by,
            'save_path': self.save_path
        })

    @staticmethod
    def is_duplicated(filename):
        res = Docx.query.get(filename)
        if res is None:
            return False
        return True

    def __init__(self, **kwargs):
        super(Docx, self).__init__(**kwargs)

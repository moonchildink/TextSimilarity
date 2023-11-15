from . import db
import datetime
from flask import jsonify


class Docx(db.Model):
    __tablename__ = 'docx'

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(64), unique=True)
    upload_time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    timestamp = db.Column(db.String(16), nullable=False)
    client_ip = db.Column(db.String(32), nullable=False)

    def to_json(self):
        return jsonify({
            'id': self.id,
            'file_path': self.file_path,
            'upload_time': self.upload_time,
            'time_stamp': self.timestamp,
            'client_ip': self.client_ip
        })

    def __init__(self, **kwargs):
        super(Docx, self).__init__(**kwargs)

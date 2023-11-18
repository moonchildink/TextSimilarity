import os
from app import creat_app, db
from flask_migrate import Migrate, upgrade
from app.model import Docx

os_name = os.name
app = creat_app(os_name=os_name)

migrate = Migrate(app, db)


# @app.shell_context_processors
# def make_shell_context():
#     return dict(db=db, Docx=Docx)


with app.app_context():
    db.create_all()

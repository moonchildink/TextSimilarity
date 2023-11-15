from flask import Flask
from config import config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def creat_app(config_name='default'):
    """
    工厂函数，在进行初始化时使用default参数
    :param config_name:
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    # 注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    return app

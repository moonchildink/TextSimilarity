import os


class Config:
    JSON_AS_ASCII = True
    MAX_CONTENT_LENGTH = 5 * 1000 * 1000
    # ALLOWED_EXTENSION = ['docx', 'doc', 'txt']
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'vz\x92\xf1\xa5\xfc7\xef\xe1\xa9\xa6\xd0\xcd\xad\xd0\x81\x14/\x07F\xe1\x0f\x90\x8c'
    ALLOWED_EXTENSION = ['docx', 'doc', 'txt']
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    MAX_FILENAME_LENGTH = 64
    @staticmethod
    def init_app(app):
        pass


class DeploymentConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    DEBUG = True
    UPLOAD_FOLDER = r'D:\code\Python\TextSimilarity\UploadFolder'
    TEMP_FILE_DIR = r'D:\code\Python\TextSimilarity\temp_file'
    HOSTNAME = '127.0.0.1'
    PORT = '3306'
    USERNAME = 'root'
    PASSWORD = os.environ.get('MYSQL_PASSWORD')
    DATABASE = "new_schema"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?"
                               f"charset=utf8mb4")


config = {
    'development': DevelopmentConfig,
    'deploy': DeploymentConfig,
    'default': DevelopmentConfig
}

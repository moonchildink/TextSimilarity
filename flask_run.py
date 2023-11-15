# import os
#
# from flask import Flask, request, render_template
# from werkzeug.utils import secure_filename
#
# import config
# from similarity import SimhashSimilarity, CosineSimilarity, read_file, process_input
#
# app = Flask(__name__)
# # 添加配置文件
# app.config.from_object(config)
# app.config.from_pyfile('config.py')
#
#
# # 注册蓝图模块
# # app.register_blueprint(bp)
#
# @app.route('/')
# def index():
#     # 在这个函数之中将页面返回
#     return render_template("index.html")
#
#
# def is_file_extension_allowed(filename: str) -> bool:
#     if filename.rsplit('.', 1)[-1].lower() in config.ALLOWED_EXTENSION:  # 获取文件的扩展名
#         return True
#     else:
#         return False
#
#
# @app.route("/text/file/", methods=["GET", "POST"])
# def uploadFile():
#     file1 = request.files.get("file1")
#     file2 = request.files.get("file2")
#     if is_file_extension_allowed(file1.filename) and is_file_extension_allowed(file2.filename):
#         fileList = os.listdir(config.UPLOAD_FOLDER)
#         num = fileList.count(file1.filename)
#         if num > 0:
#             file1.filename = file1.filename.split('.')[0] + '({0})'.format(num) + '.txt'
#         num = fileList.count(file2.filename)
#         if num > 0:
#             file2.filename = file2.filename.split('.')[0] + '({0})'.format(num) + '.txt'
#         if file1 and file2:
#             if is_file_extension_allowed(file1.filename) and is_file_extension_allowed(file2.filename):
#                 file1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file1.filename)))
#                 file2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file2.filename)))
#                 text1 = read_file(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file1.filename)))
#                 text2 = read_file(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file2.filename)))
#                 return str(process_input(text1, text2))
#             else:
#                 return "Error"
#
#
#
# # 此路由用于获取用户输入的文本
# @app.route("/text/", methods=["GET", "POST"])
# def getSimilarity():
#     text1 = request.form.get("text1")
#     text2 = request.form.get("text2")
#     print(text1, text2)
#     res = process_input(text1, text2)
#     print(res)
#     return res
#
#
# if __name__ == '__main__':
#     # webbrowser.open("http://127.0.0.1:5000")
#     # app.run()
#     if os.name == 'nt':  # 如果当前系统环境为Windows，那么运行开发时配置
#         app.run()
#     elif os.name == 'posix':  # 如果当前运行环境为Linux，那么运行部署时配置
#         app.run()


import os
from app import creat_app, db

os_name = os.name
if os_name == 'nt':
    app = creat_app()
elif os_name == 'posix':
    app = creat_app(config_name='deploy')

with app.app_context():
    db.create_all()

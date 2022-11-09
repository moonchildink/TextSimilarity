import os
import webbrowser

from flask import Flask, redirect, request, render_template, flash
from werkzeug.utils import secure_filename

import config
from main import SimhashSimilarity, CosineSimilarity, readFile, ProcessInput

app = Flask(__name__)
# 添加配置文件
app.config.from_object(config)
app.config.from_pyfile('config.py')


# 注册蓝图模块
# app.register_blueprint(bp)

@app.route('/')
def index():
    # 在这个函数之中将页面返回
    return render_template("index.html")


def isFileExtensionAllowed(filename: str) -> bool:
    if filename.rsplit('.', 1)[-1].lower() in config.ALLOWED_EXTENSION:  # 获取文件的扩展名
        return True
    else:
        return False


@app.route("/text/file/", methods=["GET", "POST"])
def uploadFile():
    file1 = request.files.get("file1")
    file2 = request.files.get("file2")
    fileList = os.listdir(config.UPLOAD_FOLDER)
    num = fileList.count(file1.filename)
    if num > 0:
        file1.filename = file1.filename.split('.')[0]+'({0})'.format(num)+'.txt'
    num = fileList.count(file2.filename)
    if num > 0:
        file2.filename = file2.filename.split('.')[0]+'({0})'.format(num)+'.txt'
    if file1 and file2:
        if isFileExtensionAllowed(file1.filename) and isFileExtensionAllowed(file2.filename):
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file1.filename)))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file2.filename)))
            text1 = readFile(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file1.filename)))
            text2 = readFile(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file2.filename)))
            return str(ProcessInput(text1, text2))
        else:
            return "Error"


# 此路由用于获取用户输入的文本
@app.route("/text/", methods=["GET", "POST"])
def getSimilarity():
    text1 = request.form.get("text1")
    text2 = request.form.get("text2")
    print(text1, text2)
    res = ProcessInput(text1, text2)
    print(res)
    return res




if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run()

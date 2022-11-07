import os
import webbrowser
from flask import Flask, jsonify, url_for, redirect, request, render_template,flash
import config
import json
from werkzeug.utils import secure_filename
from main import SimhashSimilarity,CosineSimilarity


app = Flask(__name__)
# 添加配置文件
app.config.from_object(config)


# 注册蓝图模块
# app.register_blueprint(bp)

@app.route('/')
def index():
    # 在这个函数之中将页面返回
    return render_template("index.html")


def isFileExtensionAllowed(filename:str)->bool:
    if filename.rsplit('.',1)[-1].lower() in config.ALLOWED_EXTENSION:   # 获取文件的扩展名
        return True
    else:
        return False


@app.route("/text/file/",methods = ["GET","POST"])
def uploadFile():
    if request.method == "POST":
        flash("No file part")
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        flash('no selected file')
    if file and isFileExtensionAllowed(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))    # 最终保存文件





# 此路由用于获取用户输入的文本
@app.route("/text")
def getSimilarity():
    text = request.args.get("text")
    # print(text)
    # return "success"
    if len(text)<100:
        similarity = CosineSimilarity(text)
        return similarity



if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000")
    app.run()

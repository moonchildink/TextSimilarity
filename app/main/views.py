import random
import string
from . import main
from flask import render_template, request, current_app, jsonify
import os
from .errors import unsupported_media_type, arg_required
from ..Convertor import Convertor
from ..SimhashSimilarity import SimhashSimilarity
from ..CosineSimilarity import CosineSimilarity
from ..model import Docx
from datetime import datetime
from .. import db
from app.Docx import Document


def is_file_extension_allowed(filename: str) -> bool:
    if filename.rsplit('.', 1)[-1].lower() in current_app.config['ALLOWED_EXTENSION']:  # 获取文件的扩展名
        return True
    else:
        return False


def convert_file_type(file_path):
    """
    如果为.doc文件，需要将文件转换成为.docx文件
    :return:
    """
    if file_path.endswith('.doc'):
        output_filepath = os.path.join(file_path.rsplit('.', 1)[0], '.docx')
        Convertor.convert(file_path, output_filepath)
        return output_filepath
    return file_path


def process_input(text1, text2):
    """
    :todo 该函数还需要进一步丰富，因为我们需要返回两个段落之中具体相似的部分
    :param text1:
    :param text2:
    :return:
    """
    if len(text1) < 100 and len(text2) < 100:
        return str(CosineSimilarity(text1, text2).similarity)
    else:
        return SimhashSimilarity(text1, text2).get_similarity


@main.route('/')
def index():
    return render_template(r'index.html')


@main.route('/upload_file', methods=['POST'])
def upload_file():
    """
    上传文件
    :return: no return
    """
    file1 = request.files.get('file1')
    if file1 is None:
        res = arg_required('You need to upload a file')
        return res

    if is_file_extension_allowed(file1.filename):
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.mkdir(current_app.config['UPLOAD_FOLDER'])
        # 对过长的文件名进行处理
        file1_save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file1.filename)
        if len(file1_save_path) > 64:
            rename = str(int(datetime.timestamp(datetime.utcnow())))[-5:] + random.choice(string.ascii_letters)
            file1_save_path = os.path.join(rename + file1.filename.rsplit('.', 1)[-1])
        file1.save(file1_save_path)
        file1_path = convert_file_type(file1_save_path)
        time = datetime.utcnow()
        time_stamp = str(int(datetime.timestamp(time)))
        client_ip = str(request.remote_addr)
        doc = Docx(file_path=file1_path, upload_time=time, timestamp=time_stamp, client_ip=client_ip)
        db.session.add(doc)
        db.session.commit()
        return doc.to_json()
    else:
        info = (f"request file types are showing as bellow:{current_app.config.ALLOWED_EXTENSION},"
                f"while your file are {file1.filename.rsplit('.', 1)[-1]}")
        res = unsupported_media_type(info=info)
        return res


@main.route('/my_file', methods=['GET'])
def get_my_file():
    """
    :return: 用户远程IP地址下的所有文件名称，以供用户进行选择。
    """
    request_ip = request.remote_addr
    file_list = Docx.query.filter_by(client_ip=request_ip).all()

    file_name_list = [i.file_path for i in file_list]
    return jsonify({
        'filenames': file_name_list
    })


@main.route('/most_similar', methods=['GET'])
def get_most_similar():
    """
    在我的文件中查找最相似的文件
    :return:
    """
    request_ip = request.remote_addr
    file_list = Docx.query.filter_by(client_ip=request_ip).all()
    documents_list = []
    for file in file_list:
        documents_list.append(Document(file.file_path))

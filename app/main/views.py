import json
import random
import string
import sqlalchemy.exc
from . import main
from flask import render_template, request, current_app, jsonify
import os
from .errors import unsupported_media_type, arg_required, file_not_found
from ..Convertor import Convertor
from ..SimhashSimilarity import SimhashSimilarity
from ..CosineSimilarity import CosineSimilarity
from ..model import Docx
from datetime import datetime
from .. import db
from app.Docx import Documents, Document
from docx import Document as docx_document


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
        output_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path.rsplit('.', 1)[0] + '.docx')
        Convertor.convert(file_path, output_filepath)
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], file_path))
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

        file1_path = convert_file_type(file1.filename)

        if len(file1.filename) > current_app.config['MAX_FILENAME_LENGTH']:
            rename = str(int(datetime.timestamp(datetime.utcnow())))[-5:] + random.choice(
                string.ascii_letters) + '.docx'
        else:
            rename = file1.filename
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], rename)

        time = datetime.utcnow()
        time_stamp = str(int(datetime.timestamp(time)))
        client_ip = str(request.remote_addr)
        file1.save(save_path)
        doc = docx_document(save_path)
        author = doc.core_properties.author if hasattr(doc.core_properties, 'author') else None
        created = doc.core_properties.created if hasattr(doc.core_properties, 'created') else None
        modified = doc.core_properties.modified if hasattr(doc.core_properties, 'modified') else None
        last_save_by = doc.core_properties.last_modified_by if hasattr(doc.core_properties,
                                                                       'last_modified_by') else None
        doc = Docx(save_path=save_path, filename=file1_path, upload_time=time, timestamp=time_stamp,
                   client_ip=client_ip, author=author, created=created, modified=modified, last_saved_by=last_save_by)
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

    # li = []
    # for file in file_list:
    #     li.append(file.to_json())

    # 返回文件名
    filenames = []
    authors = []
    for file in file_list:
        filenames.append(file.filename)
        if file.author is not None:
            authors.append(file.author)
        else:
            authors.append('No author info.')

    return jsonify({
        'file_count': len(file_list),
        'filenames': filenames,
        'authors': authors
    })


@main.route('/most_similar', methods=['GET'])
def get_most_similar():
    """
    在我的文件中查找最相似的文件
    :return:
    """
    request_ip = request.remote_addr
    file_list = Docx.query.filter_by(client_ip=request_ip).all()
    documents_list = [document.file_path for document in file_list]
    documents = Documents(documents_list)

    key, value = documents.get_most_similar

    return jsonify({
        'most_similar': str((key, value))
    })


@main.route('/get_docx/<int:file_index>', methods=['GET', 'POST'])
def get_docx(file_index):
    file = Docx.query.get(file_index)
    if file is None:
        info = f"the document with index = {file_index} you request is not found in server"
        res = file_not_found(info=info)
        return res
    else:
        document = Document(file.filename)
        res = file.to_json()
        json_dict = json.loads(res)
        json_dict['text'] = document.text
        return jsonify(json_dict)

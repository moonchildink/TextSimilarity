"""
用于实现将.doc文件转换为.docx文件
"""

import subprocess


class Convertor:
    def __init__(self, input_doc_path):
        self.input_doc_path = input_doc_path

    def convert_doc_to_docx(self, output_path):
        subprocess.run(['unoconv', '-f', 'docx', '-o', output_path, self.input_doc_path])
        return output_path

    @staticmethod
    def convert(input_doc, output_docx):
        subprocess.run(['unoconv', '-f', 'docx', '-o', output_docx, input_doc])

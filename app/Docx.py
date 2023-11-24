import os.path
from .SimhashSimilarity import SimhashSimilarity
# from ConsineSimilarity import ConsineSimilarity
from .CosineSimilarity import CosineSimilarity
from bs4 import BeautifulSoup
import mammoth
from flask import current_app


class Txt:
    def __init__(self, filepath):
        self.filepath = filepath
        try:
            with open(filepath, 'r') as file:
                self.content = file.read()
        except FileNotFoundError as e:
            pass

    @property
    def text(self):
        return self.content


class Document:
    def __init__(self, file_path):
        self.input_path = file_path
        self.output_html_path = os.path.join(current_app.config['TEMP_FILE_DIR'],
                                             self.input_path.rsplit('\\', 1)[-1].split('.')[0] + '.html')
        self.output_md_path = self.output_html_path.rsplit('.', 1)[0] + '.md'
        try:
            self.convert_docx_to_html()
            self.convert_docx_to_markdown()
        except FileNotFoundError as e:
            pass
            # self.text = None
        except Exception as e:
            pass

    def convert_docx_to_html(self):
        custom_style = 'b=>i'
        with open(self.input_path, 'rb') as docx_file:
            result = mammoth.convert_to_html(docx_file, style_map=custom_style)

        text = result.value
        with open(self.output_html_path, 'w+', encoding='utf-8') as html_file:
            html_file.write(text)

    def convert_docx_to_markdown(self):
        with open(self.input_path, 'rb') as docx_file:
            result = mammoth.convert_to_markdown(docx_file)
        with open(self.output_md_path, 'w+', encoding='utf-8') as markdown_file:
            markdown_file.write(result.value)

    @property
    def text(self):
        """
        :return:all texts in document,in the format of list
        """
        try:
            with open(self.output_html_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
        except FileNotFoundError as e:
            pass
        soup = BeautifulSoup(html_content, 'html.parser')
        elements = soup.find_all(['p', 'li', 'label'])
        texts = [element.get_text().strip() for element in elements]
        main_text = '\n'.join(texts)

        return main_text


class Documents:
    """
    计算文本之间的相似度方法还有很多，还可以再添加其他的计算方法。
    """

    def __init__(self, documents_list):
        """
        :param documents_list: 传入文件名列表
        """
        self.sorted_simhash_dict = None
        self.sorted_cosine_dict = None
        self.documents = documents_list
        self.file_path = [os.path.join(current_app.config['UPLOAD_FOLDER'], document) for document in
                          self.documents]
        self.dic = dict()

        for idx, elem in enumerate(self.documents):
            print(elem)
            temp = Document(self.file_path[idx])
            self.dic[elem] = temp.text

        self.simhash_dict = dict()
        self.get_simhash_similarity()

        self.cosine_dict = dict()
        self.get_cosine_similarity()

        self.sorted_cosine_dict = sorted(self.cosine_dict.items(), key=lambda item: item[1], reverse=True)
        self.sorted_simhash_dict = sorted(self.simhash_dict.items(), key=lambda item: item[1], reverse=True)

    def get_simhash_similarity(self):
        for key, value in self.dic.items():
            for key2, value2 in self.dic.items():
                if key != key2:
                    dict_key = (key, key2)
                    self.simhash_dict[dict_key] = SimhashSimilarity(value, value2).get_similarity

    def get_cosine_similarity(self):
        for key, value in self.dic.items():
            for key2, value2 in self.dic.items():
                if key != key2:
                    dict_key = (key, key2)
                    self.cosine_dict[dict_key] = CosineSimilarity(value, value2).similarity

    def get_simhash_ranked_list(self):
        return self.sorted_simhash_dict

    def get_cosine_ranked_list(self):
        return self.sorted_cosine_dict

    @property
    def get_most_similar(self):
        first_key, first_value = next(iter(self.sorted_cosine_dict))
        return first_key, first_value

    @property
    def simhash_similarity(self):
        return self.simhash_dict

    @property
    def cosine_similarity(self):
        return self.cosine_dict

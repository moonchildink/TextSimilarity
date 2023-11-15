import jieba
import jieba.analyse
from sklearn.metrics.pairwise import cosine_similarity


class CosineSimilarity:
    def __init__(self, string1, string2):  # 如何判断用户输入的是一段文本还是一个文件路径????
        # 先假设用户输入的一段文本，首先去空格，去标点符号
        self.text1 = self.preprocessing(string1)
        self.text2 = self.preprocessing(string2)

    @staticmethod
    def preprocessing(text: str) -> str:
        return text.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')

    @staticmethod
    def one_hot(word_dict, key_words):  # 预处理,生成离散的oneHot()编码
        one_hot_code = [0 for _ in range(len(word_dict))]
        for word in key_words:
            one_hot_code[word_dict[word]] = 1
        return one_hot_code

    # 计算余弦相似度
    @property
    def similarity(self):
        # extract_tags本身返回的就是出现频率最高的20个词,那么接下来的union至多40个单词
        text1 = jieba.analyse.extract_tags(self.text1)
        text2 = jieba.analyse.extract_tags(self.text2)

        union = set(text1).union(set(text2))  # 去重取并集

        # 为每个词添加索引,使用字典
        word_dict = dict(zip(union, range(0, len(union))))
        text1OneHotCode = self.one_hot(word_dict, text1)
        text2OneHotCode = self.one_hot(word_dict, text2)
        try:
            sim = cosine_similarity([text1OneHotCode, text2OneHotCode])
            return sim[1][0] * 100
        except Exception as e:
            print(e)
            return 0.0

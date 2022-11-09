from simhash import Simhash
from simhash import SimhashIndex
import re
import jieba
import jieba.analyse  # 基于TF-IDF算法地关键词提取,会返回权重最大的几个词汇
from sklearn.metrics.pairwise import cosine_similarity


# jieba同样提供了按词性进行分词,可以尝试

class CosineSimilarity:
    def __init__(self, string1, string2):  # 如何判断用户输入的是一段文本还是一个文件路径????
        # 先假设用户输入的一段文本，首先去空格，去标点符号
        self.text1 = self.preprocessing(string1)
        self.text2 = self.preprocessing(string2)

    @staticmethod
    def preprocessing(text: str) -> str:
        return text.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')

    @staticmethod
    def oneHot(wordDict, keyWords):  # 预处理,生成离散的oneHot()编码
        oneHotCode = [0 for _ in range(len(wordDict))]
        for word in keyWords:
            oneHotCode[wordDict[word]] = 1
        return oneHotCode

    # 计算余弦相似度
    @property
    def Similarity(self):
        # extract_tags本身返回的就是出现频率最高的20个词,那么接下来的union至多40个单词
        text1 = jieba.analyse.extract_tags(self.text1)
        text2 = jieba.analyse.extract_tags(self.text2)

        union = set(text1).union(set(text2))  # 去重取并集

        # 为每个词添加索引,使用字典
        wordDict = dict(zip(union, range(0, len(union))))
        text1OneHotCode = self.oneHot(wordDict, text1)
        text2OneHotCode = self.oneHot(wordDict, text2)

        # 计算余弦相似度,使用scipy包里的cosine_similarity
        # return 1 - cosine_similarity([text1OneHotCode, text2OneHotCode])
        try:
            sim = cosine_similarity([text1OneHotCode, text2OneHotCode])
            # print("文本相似度:%.2f%%" % (sim[1][0] * 100))
            # print()
            return sim[1][0]*100
        except Exception as e:
            print(e)
            return 0.0


class SimhashSimilarity:
    """
        调用Simhash库,计算文本相似度
    """

    def __init__(self, string1, string2):
        self.text1 = string1
        self.text2 = string2

    @property
    def getSimilarity(self):
        # 生成Simhash对象
        simhash1 = Simhash(self.text1)
        simhash2 = Simhash(self.text2)

        # 计算海明距离
        distance = simhash1.distance(simhash2)
        # 计算相似度
        similarity = 1 - distance / 64
        print("文本相似度:%.2f%%" % (similarity * 100))
        print()
        return similarity


def readFile(filePath):
    with open(filePath, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace('\n', '')
    text = ''.join(re.findall('[\u4e00-\u9fa5]', text))
    return text


def ProcessInput(text1, text2):
    if len(text1) < 100 and len(text2) < 100:
        return str(CosineSimilarity(text1, text2).Similarity)
    else:
        return SimhashSimilarity(text1, text2).getSimilarity

from simhash import Simhash
from simhash import SimhashIndex


class SimhashSimilarity:
    """
        调用Simhash库,计算文本相似度
    """

    def __init__(self, string1, string2):
        self.text1 = string1
        self.text2 = string2

    @property
    def get_similarity(self):
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

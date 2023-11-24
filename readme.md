# Python实现的Word文本相似度查询



## 主要思路与方法

### 查询相似度的实现


1. 使用余弦定理计算两段文本之间的相似度.适用于短文本.此处涉及到两个python库:
    1. jieba: 中文分词
    2. `scipy.spatial.distance.cosine`,主要是余弦定理的计算,此处也可以自己手动造轮子来计算
    3. 主要思路:
        1. 读取用户输入的文本
        2. 分词
        3. 对两段文本进行预处理,取两个文本主要词的并集,并且根据该并集生成
            每一段文本的特征向量
        4. 接下来便是对特征向量计算余弦值,也就是我们需要的相似度
2. simhash方法:
    1. 这部分则主要适用于长文本,对于使用余弦定理来计算大量特征向量之间的相似度而言时空复杂度较高
    2. 直接使用了网上开源的simhash算法,之后进行了封装

### 后端服务请求的实现

后端主要使用了Flask框架，主要实现了以下功能：

1. 接受用户上传的文件并保存到本地，将文件相关信息存储到数据库之中。因为没考虑特别复杂的需求，仅设计了Docx一个表，其中包含的表单项如下：

   ![image-20231124121830319](https://raw.githubusercontent.com/moonchildink/image/main/imgs202311241218936.png)

2. 文件类型转换。目前常用的Word格式为`.docx`，全称为Office Open XML，更加开放，方便进行传输、处理。而现在仍然有相当一部文档使用`.doc`格式，这种格式以二进制方式存储，难以进行处理。后端在接收到`.doc`文件之后，要首先将其转换为`.docx`文件。

3. 获取用户文件：此处没有设计登录或者是其他的用户相关功能，当用户想查询所上传的文件时，使用IP地址来进行筛选。

4. 返回最相似的文件；

5. 获取指定文件



### 前端的实现与功能

前端使用了jQuery与Bootstrap实现。

1. 初始页面如下：![image-20231124122549408](https://raw.githubusercontent.com/moonchildink/image/main/imgs202311241225503.png)

2. 点击选择文件可以上传多个文件![image-20231124123457795](https://raw.githubusercontent.com/moonchildink/image/main/imgs202311241234847.png)
3. 点击我的文件可以查看已经上传的文件，此处文件可能较多，添加了分页功能。![image-20231124123615217](https://raw.githubusercontent.com/moonchildink/image/main/imgs202311241236281.png)

4. 点击TextSimilarity可以查看相似的文件：![image-20231124123751593](https://raw.githubusercontent.com/moonchildink/image/main/imgs202311241237689.png)

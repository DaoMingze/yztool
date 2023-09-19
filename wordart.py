import jieba


def preprocess(ctx):
    import re

    pattern = re.compile(r'\t|\n|\.|-|:|;|\)|\(|\?|" ')
    ctx = re.sub(pattern, '', ctx)
    return ctx


def readfile(path: str, suff: str = "txt"):
    with open(path + "." + suff, mode="r", encoding="utf-8") as file:
        f = file.read()
    return f


def genpic(font: str = "serif", name: str = "test", ctx=[], stopword=""):
    from wordcloud import WordCloud

    wc = WordCloud(
        # 设置字体旋转度，0-1，1为垂直
        # prefer_horizontal=1,
        # 设置词云的中文字体所在路径，不指定就会出现乱码
        font_path='/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc',
        # 设置宽
        width=1280,
        # 设置高
        height=640,
        # 设置背景色
        background_color='white',
        max_words=100,
        # 字号上限
        max_font_size=300,
        # 字号下限
        min_font_size=30,
        # 词频与放大程度的相关性
        relative_scaling=0.7,
        stopwords=stopword,
        mode='RGBA',
        mask=mask,
    )
    # wc.generate(ctx)  # 加载词云文本
    wc.generate_from_frequencies(ctx)
    wc.to_file(name + ".png")  # 保存词云文件


def wordcount(ctx: list, top: int = 10):
    from collections import Counter  # 词频统计库

    counts = Counter(ctx)  # 对分词做词频统计
    counts_top = counts.most_common(top)  # 获取前n最高频的词
    # print(counts_top)  # 输出检查
    return counts_top


def cleanlist(ctx, list):
    for i in list:
        for x in range(ctx.count(i)):
            ctx.remove(i)
    return ctx


def maskpic(path: str = ""):
    import numpy as np
    from PIL import Image

    img = Image.open(path)
    mask = np.array(img)  # 将图片转换为数组
    return mask


def writefile(name: str, context: str):
    with open(name + ".txt", mode="w", encoding="utf-8") as file:
        file.write(context)


if __name__ == "__main__":
    filename = input("请输入纯文本格式文件名：")
    f = readfile(filename)
    f = preprocess(f)
    jieba.load_userdict("lis_dict.txt")
    ls = jieba.lcut(f)  # 生成分词列表
    ls = cleanlist(ls, ['与', ' '])
    text = dict(wordcount(ls, 1000))
    writefile(filename + "处理后", str(text))
    mask = maskpic("2023/books1280.png")
    genpic(name=filename + "word", ctx=text)
'''
    with open("处理后1.txt", mode="r", encoding="utf-8") as test:
        man = json.load(test)
    genpic(name="1205man", ctx=man)
'''

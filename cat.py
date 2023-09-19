import json

import requests
from lxml import etree

# 定义一个字典，用以存放关键词


def savefile(filename, context, suff: str = "txt"):
    """
    默认保存为json
    """
    with open(filename + "." + suff, "w", encoding="utf-8") as file:
        # json.dump(context, file)
        file.write(str(context))


def get(url=str, keyword: str = ""):
    """
    网页获取方法
    """
    # 进行搜索并下载搜索页面
    fakeua = {
        "Accept": "text/html, application/xhtml+xml, */*",
        "Accept-Language": "en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) \
            Gecko/20100101 Firefox/108.0",
    }
    timeout = 60
    # ↑虚假UA（用户代理），以免抓取频率过高导致报错
    Page = requests.get(
        url + keyword,
        headers=fakeua,
        timeout=timeout,
    )
    # ↑引用request库，抓取网页
    html = etree.HTML(Page.text)
    return html


if __name__ == "__main__":
    res = {}
    with open("universities.txt", "r", encoding="utf-8") as file:
        querylist = json.load(file)
    for i in querylist:
        html = get("https://cn.bing.com/search?q=", i + " 本科招生信息网")
        url = html.xpath("//li[1]/div[1]/h2/a/@href")
        res[i] = url[0]
    savefile("大学", res)
    print("抓取并写入完成，共计%s条" % len(res))

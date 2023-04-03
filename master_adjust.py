import requests


def post(url=str, keyword: str = ""):
    """
    网页获取方法
    """
    # 进行搜索并下载搜索页面
    fakeua = {
        "Accept": "text/html, application/xhtml+xml, */*",
        "Accept-Language": "en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3",
    }
    timeout = 60
    # ↑虚假UA（用户代理），以免抓取频率过高导致报错
    Page = requests.post(
        url + keyword,
        headers=fakeua,
        timeout=timeout,
    )
    # ↑引用request库，抓取网页
    return Page


def savefile(filename, context, suff: str = "json"):
    """
    默认保存为json
    """
    with open(filename + "." + suff, "w", encoding="utf-8") as file:
        file.write(context)


def postdict(words: str = "大学", page: str = "1"):
    post = (
        "?mhcx=1"
        + "&dwmc2="
        + words
        + "&data_type=json&agent_from=web"
        + "&pageid="
        + page
    )
    # 模糊查询
    return post


if __name__ == "__main__":
    url = "https://yz.chsi.com.cn/sytj/stu/tjyxqexxcx.action"
    words = input("模糊检索词：")
    page = int(input("页数："))
    ctx = []
    postword = postdict(words, str(page))
    for i in range(page):
        context = list(post(url, postword))
        ctx += context
    savefile(words + "调剂意向信息", str(ctx))

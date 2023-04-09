# -*- coding:utf-8 -*-
import requests


def login(user: str, pw: str):
    _url = "https://account.chsi.com.cn/passport/login\
                ?entrytype=yzgr&service=https%3A%2F%2Fyz.chsi.com.cn%2F\
                j_spring_cas_security_check"
    fakeua = {
        "Accept": "text/html, application/xhtml+xml, */*",
        "Accept-Language": "en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3",
    }
    body = {
        "username": user,
        "password": pw,
        "lt": "LT-939006-Ygsqj1fTJmd9YtRFFCN1pVfIC5gn1F-cas",
        "_eventId": "submit",
        "submit": "%E7%99%BB%C2%A0%C2%A0%E5%BD%95",
    }
    try:
        session = requests.session()
        cookie_jar = session.post(url=_url, data=body, headers=fakeua).cookies
        cookie_t = requests.utils.dict_from_cookiejar(cookie_jar)
        return cookie_t
    except Exception as err:
        print('获取cookie失败：\n{0}'.format(err))


def post(url=str, keyword: str = ""):
    """
    网页获取方法
    """
    # 进行搜索并下载搜索页面
    fakeua = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,\
            image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,\
            en-US;q=0.3,en;q=0.2",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) \
            Gecko/20100101 Firefox/102.0",
    }
    timeout = 60
    # ↑虚假UA（用户代理），以免抓取频率过高导致报错
    Page = requests.post(
        url + keyword,
        headers=fakeua,
        cookies=cookie,
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
    # url = "https://yz.chsi.com.cn/sytj/stu/tjyxqexxcx.action"
    url = "https://yz.chsi.com.cn/sytj/stu/sytjqexxcx.action"
    cookie = login("13980449934", "XXWwizard81*")
    words = "图书情报"  # input("模糊检索词：")
    page = 2  # int(input("页数："))
    ctx = []
    postword = postdict(words, str(page))
    print(url + postword)
    '''for i in range(page):
        context = list(post(url, postword))
        ctx += context
    '''
    print(cookie)
    print(post(url, postword))
    savefile(words + "调剂意向信息", str(post(url, postword)), "html")

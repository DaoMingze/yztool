import json
import os

import requests
from lxml import etree

# ↑引用xpath库，分析网页元素

right_path = __file__.rstrip(os.path.basename(__file__))  # 获取当前文件的所在路径
os.chdir(right_path)  # 将工作路径改至目标路径


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


def savefile(filename, context, suff: str = "json"):
    """
    默认保存为json
    """
    with open(filename + "." + suff, "w", encoding="utf-8") as file:
        file.write(context)


def readfile(name=str):
    with open(name + ".json", "r", encoding="utf-8") as file:
        context = json.load(file)
    return context


def queryuniversities(html):
    # ↓构造xpath路径，抓取元素 html.xpath("")
    universities_name = html.xpath(
        "//table[@class='ch-table']/tbody[1]/tr//td//form[1]//a[1]/text()"
    )
    universities_url = html.xpath(
        "//table[@class='ch-table']/tbody[1]/tr//td//form[1]/a/@href"
    )
    universitieslist = list(zip(universities_name, universities_url))
    return universitieslist


def queryprofession(dict):
    # allprofession = []
    profession_id = []
    for i in dict:
        k = dict.get(i)
        html = get(url + k)
        profession_url = html.xpath(
            "//table[contains(@class,'ch-table more-content')]\
                /tbody[1]/tr//td[8]/a/@href"
        )
        university_name = []
        for x in range(len(profession_url)):
            university_name.append(i)
            a = str(profession_url[x]).replace("/zsml/kskm.jsp?id=", "")
            profession_id.append(a)
        print("%s已经完成" % (i))
    return profession_id


def queryinfo(list):
    finalinfo = ()
    query = "/zsml/kskm.jsp?id="
    for i in list:
        html = get(url + query + i)
        unversity = html.xpath("(//td[@class='zsml-summary'])[1]/text()")
        school = html.xpath("(//td[@class='zsml-summary'])[3]/text()")
        profession = html.xpath("(//td[@class='zsml-summary'])[4]/text()")
        dirct = html.xpath("(//td[@class='zsml-summary'])[6]/text()")
        quota = html.xpath("(//td[@class='zsml-summary'])[8]/text()")
        major1 = html.xpath("(//tbody[@class='zsml-res-items']//td)[3]/text()")
        major2 = html.xpath("(//tbody[@class='zsml-res-items']//td)[4]/text()")
        finalinfo += tuple(
            zip(unversity, school, profession, dirct, quota, major1, major2)
        )
    return finalinfo


def task_one(name=str, ml: str = "12", xk: str = "1205", page: int = 2):
    # 第一步，获取招生单位名单
    query = query = "?mldm=" + ml + "&yjxkdm=" + xk
    # 翻页，不想去做判断里，就手动输入
    universitieslist = []
    # 新建空的招生单位字典
    for x in range(1, page + 1):
        html = get(url + "/zsml/queryAction.do" + query, "&pageno=" + str(x))
        universitieslist += queryuniversities(html)
    # 抓取{page}页的招生单位及其详情，因为程序默认从0开始，而实际分页从1开始，所以平移了一下
    savefile(name, json.dumps(dict(universitieslist)))
    # 可以保存为csv（逗号分隔值）方便导入excel
    # print("共生成%d条%s信息" %(len(universitieslist),task1))
    # ↑检查抓取数据


def task_two(name=str):
    universitiesdict = readfile(task)
    profession_id = queryprofession(universitiesdict)
    # 我默认一个招生单位的一个学科（四位代码）不会有30条以上的专业、方向，所以没写翻页。如果有，按上面招生单位的处理。
    # savefile(name, str(allprofession))
    savefile(task + "_index", json.dumps(profession_id))
    return print("第二步完成，若信息有误则取消注释进行检查\n下面进行第三步，请稍候")


def task_three(name):
    allprofession = readfile(task + "_index")
    # allprofession = testdict
    finalinfo = queryinfo(allprofession)
    savefile(name, json.dumps(list(finalinfo)))
    print("第三步已完成，生成%s文件，请查收" % (name))


if __name__ == "__main__":
    url = "https://yz.chsi.com.cn"
    print("其他学科根据门类代码修改ml，学科代码修改xk")
    print("例如图情学硕：ml=12，xk=1205\n而图情专硕：ml=zyxw，xk=1255")
    task = input("采集项目名：")
    ml = input("ml=")
    xk = input("xk=")
    page = int(input("共计多少页，不清楚就去研招网看一下："))
    task_one(task, ml, xk, page)
    task_two(task + "完整专业目录")
    task_three(task + "详细信息")

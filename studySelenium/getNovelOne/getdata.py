import textwrap
import time
from contextlib import contextmanager
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
#
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import requests as rq
from bs4 import BeautifulSoup
from opencc import OpenCC
import os


LF = '\n'
CRLF = '\r\n'
CR = '\r'


@contextmanager
def make_chromw_driver() -> Chrome:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")

    driver = Chrome(ChromeDriverManager().install(), options=options)
    yield driver
    driver.quit()


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

# 簡繁體轉換


def simplified2Traditional(ltxt):
    cc = OpenCC('s2twp')
    text = cc.convert(ltxt)
    return text


def isIgnorChar(item):
    ret = False
    if LF == item.text or CR == item.text or CRLF == item.text or '\n\n\n\n' == item.text or '\n\n\n' == item.text:
        # print(item.text)
        ret = True
    return ret


def getResultData(reslst):
    resultdic = {}
    for item in reslst:
        adata = item.find("a", href=True)
        # print(type(adata))
        try:
            lhref = adata['href']
            pos = lhref.rfind("/")
            dhref = lhref[(pos + 1):]
            # print(dhref)
            pos = dhref.rfind(".")
            dnum = int(dhref[:pos])
            # print(dhref)
            data = {
                "rowdata": adata,
                "html": dhref
            }
            # resultdic[dnum] = dhref
            resultdic[dnum] = data
            # resultdic.append(data)
            # print(lhref)
        except:
            print('An exception occurred')
    # print("resultdic=", resultdic)
    # for key, value in sorted(resultdic.items()):
    #     print("{} = {}".format(key, value))
    result = sorted(resultdic.items())
    return result


def replaceText(rowtext):
    pos = rowtext.find("ＵU看書")
    if pos < 0:
        pos = rowtext.find("UU看書")
    if pos < 0:
        pos = rowtext.find("UＵ看書")
    new_character = ""
    # print(pos)
    string = rowtext[:pos] + new_character + rowtext[pos + 21:]
    # print(string)
    return string


def getPageData(url):
    # print(url)
    response = rq.get(url)  # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text  # text 屬性就是 html 檔案
    bpage = BeautifulSoup(response.text, "lxml")
    # print(bpage.prettify())
    pagedata = bpage.find("div", {"id": "contentbox"})
    # print("-----------------------------")
    rowtext = ""
    for item in pagedata:
        if isIgnorChar(item) == False:
            # print(item.text)
            rowtext += item.text + CRLF
    # print(repr(rowtext))
    # print("-----------------------------")
    rowtext = simplified2Traditional(replaceText(rowtext))
    # print(rowtext)
    return rowtext


def formatResultData(resultdic):
    url = "https://tw.uukanshu.com"
    for idx, item in enumerate(resultdic):
        # print(idx, item)
        testdata = item
        datapack = testdata[1]
        rowdata = datapack["rowdata"]
        htmdata = datapack["html"]
        # print(rowdata)
        # print(htmdata)
        lhref = rowdata["href"]
        # print(lhref)
        eurl = url + lhref
        # print(eurl)
        title = rowdata["title"]
        # print(title)
        ftitle = '{0:04}'.format(idx + 1) + '-' + title
        # print(ftitle)
        contenttxt = getPageData(eurl)
        writeToFile(ftitle, contenttxt)
    return


def writeToFile(title, content):
    with open(f"./小說/{title}.txt", mode="w", encoding="utf-8") as f:
        f.write(content)


def getOneChapData(idx, resultlst):
    # 56287.html 第一章
    url = "https://tw.uukanshu.com"
    # print(type(resultlst))

    curridx = idx - 1
    # print(f'curridx={curridx}')
    dicdata = resultlst[curridx]
    datapack = dicdata[1]
    # print(datapack)
    rowdata = datapack["rowdata"]
    htmdata = datapack["html"]
    # print(f'rowdata={rowdata}')
    # print(f'htmdata={htmdata}')
    lhref = rowdata["href"]
    # print(lhref)
    eurl = url + lhref
    print(eurl)
    title = rowdata["title"]
    ftitle = '{0:04}'.format(curridx) + '-' + title
    print(ftitle)
    contenttxt = getPageData(eurl)
    print(contenttxt)


def getPageHTMLdata(eurl):
    response = rq.get(eurl)  # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text  # text 屬性就是 html 檔案
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.prettify())  # 把排版後的 html 印出來


def demo_get_novel2():
    mid = '33'
    #print(f'word = {word}')
    url = f"https://tw.uukanshu.com/b/{mid}/"  # PTT NBA 板
    response = rq.get(url)  # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text  # text 屬性就是 html 檔案
    soup = BeautifulSoup(response.text, "html.parser")  # 指定 lxml 作為解析器
    # print(soup.prettify())  # 把排版後的 html 印出來
    lst = soup.find("ul", attrs={"id": "chapterList"}).find_all("li")
    # print(lst)
    resultlst = getResultData(lst)
    chap = 2354
    cls()  # resultlst = getResultData(lst)
    # print(resultlst)   # print(resultlst)
    print("*****************************")
    print("*****************************")
    print("*****************************")
    getOneChapData(chap, resultlst)
    print("-----------------------------")
    print("-----------------------------")
    print("-----------------------------")
    return

    chap = 2


def demo_get_novel():
    mid = '33939'
    #print(f'word = {word}')
    url = f"https://tw.uukanshu.com/b/{mid}/"  # PTT NBA 板
    response = rq.get(url)  # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text  # text 屬性就是 html 檔案
    soup = BeautifulSoup(response.text, "html.parser")  # 指定 lxml 作為解析器
    # print(soup.prettify())  # 把排版後的 html 印出來
    # return
    # <ul id="chapterList">
    lst = soup.find("ul", attrs={"id": "chapterList"}).find_all("li")
    # print(lst)
# 56287.html 第一章
# 56288 第二章
# 56462.html 第三章

    resultlst = getResultData(lst)
    # print(resultlst)
    # return
    chap = 1758
    cls()
    print("*****************************")
    print("*****************************")
    print("*****************************")
    getOneChapData(chap, resultlst)
    print("-----------------------------")
    print("-----------------------------")
    print("-----------------------------")
    return
    formatResultData(resultdic)
    return
    adata = lst[-2].find("a")
    # print(adata['href'])
    url = "https://tw.uukanshu.com"
    eurl = url + adata['href']
    print(eurl)
    response = rq.get(eurl)  # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text  # text 屬性就是 html 檔案
    # bpage = BeautifulSoup(response.text, "lxml")  # 指定 lxml 作為解析器

    # dct = {"c": 1, "b": 3, "a": 7}
    # for key, value in sorted(dct.items()):
    #     print("{} = {}".format(key, value))

    bpage = BeautifulSoup(response.text, "html.parser")
    # print(bpage.prettify())
    pagedata = bpage.find("div", {"id": "contentbox"})
    starinfo = "=" * 40
    print(starinfo)
    # print(pagedata)
    for item in pagedata:
        if isIgnorChar(item) == False:
            print(item.text)
        # print(item.class.__name__)
        # print(type(item))
        # print(repr(item.text))
        # if '\n' in item.text or '\r' in item.text or '\n\n\n\n' in item.text:
        #     print("has n r ")
        #     # print(type(item))
        # if CRLF in item.text:
        #     print("has crlf")
        #     # print(type(item))
        # print(repr(item.text))
        # if(item.text != "") or (item.text != '\n') or (item.text != CRLF):
        #     print(item.text)
        # print(type(item).__name__)
    #     if type(item).__name__ == "NavigableString":
    #         # print(item)
    #         print(item.text)

    #     # bs4.element.Tag
    #     # print("_class is a instance of MyClass() : ", isinstance(item,bs4.element.Tag))
    #     # addata = item.find("div", attrs={"class": "ad_content"})
    #     # print(addata)
    #     # if addata != None:
    #     #     print(item)
    # # for item in lst:
    # #     print(item)
    # # print(item.text)


if __name__ == '__main__':
    # demo_get_novel()
    demo_get_novel2()

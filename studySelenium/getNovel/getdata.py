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


def demo_facebook_data():
    with make_chromw_driver() as driver:
        driver.get("https://www.facebook.com/profile.php?id=100078089262603")
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # 取得要如何拿到class
        # print(soup.prettify())
        # results = soup.find_all("div", dir="auto")
        all_results = soup.find_all("div", {'style': 'text-align: start;'})
        # print(all_results)

        idx = 0
        for content in all_results:
            if idx == 1:
                print(content.text)
            idx += 1


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
        testdata=item
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
    i = 0
    testdata = resultdic[i]
    # print(testdata)
    url = "https://tw.uukanshu.com"
    # print(type(testdata))
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
    ftitle = '{0:04}'.format(i + 1) + '-' + title
    # print(ftitle)
    contenttxt = getPageData(eurl)
    writeToFile(ftitle, contenttxt)


def writeToFile(title, content):
    with open(f"./小說/{title}.txt", mode="w", encoding="utf-8") as f:
        f.write(content)


def demo_get_novel():
    url = "https://tw.uukanshu.com/b/94859/"  # PTT NBA 板
    response = rq.get(url)  # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text  # text 屬性就是 html 檔案
    soup = BeautifulSoup(response.text, "html.parser")  # 指定 lxml 作為解析器
    # print(soup.prettify())  # 把排版後的 html 印出來
    # <ul id="chapterList">
    lst = soup.find("ul", attrs={"id": "chapterList"}).find_all("li")
    # print(lst)
    resultdic = {}
    # print(lst[1])
    resultdic = getResultData(lst)
    # print(resultdic)
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
    demo_get_novel()

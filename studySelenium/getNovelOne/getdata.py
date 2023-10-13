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
    for key, value in resultdic.items():
        print("{} = {}".format(key, value))
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


def addNewLine(text):
    line_length = 60
    lines = []
    for i in range(0, len(text), line_length):
        lines.append(text[i:i + line_length] + '\n')
    result = ""
    for x in lines:
        result += x + CRLF
    return result


def addNormal(text):
    return text


def getPageData(url):
    # print(url)
    textstr = ""
    response = rq.get(url)  # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text  # text 屬性就是 html 檔案
    bpage = BeautifulSoup(response.text, "html.parser")
    divcontent = bpage.find("div", {"id": "contentbox"})

    # print(divcontent.prettify())
    # 檢查長度
    temptext = divcontent.getText("\n\n").strip()
    # print(len(temptext))
    if(len(temptext) > 0):
        textstr = temptext
    else:
        pass

        pagedata = divcontent.find("p")

        if pagedata is not None:
            # print("000000000000000000000")
            # print(pagedata.prettify())
            textstr = pagedata.getText("\n\n")
        else:
            textstr = divcontent.find("div", {"id": "contentbox"}).getText("\n\n")
            # print("***************************")
            # print(textstr)
    print(simplified2Traditional(replaceText(textstr)))
    # if pagedata is not None:
    #     print(simplified2Traditional(replaceText(pagedata)))
    # else:
    #     pagedata = bpage.find("div", {"id": "contentbox"}).getText("\n")
    #     print(simplified2Traditional(replaceText(pagedata)))
    return
    # pagedata = bpage.find("div", {"id": "contentbox"})
    # print(pagedata)
    return
    # print("-----------------------------")
    rowtext = ""
    for item in pagedata:
        print(item.text)
        if isIgnorChar(item) == False:
            # print(item.text)
            rowtext += addNewLine(item.text)
            # rowtext += addNormal(item.text)
    # print(repr(rowtext))
    # print("-----------------------------")
    # rowtext = simplified2Traditional(replaceText(rowtext))
    rowtext = simplified2Traditional(rowtext)
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


# def getOneChapData(url, idx, resultlst):
#     # 56287.html 第一章
#     # url = "https://tw.uukanshu.com"
#     # print(type(resultlst))

#     curridx = idx - 1
#     # print(f'curridx={curridx}')
#     dicdata = resultlst[curridx]
#     datapack = dicdata[1]
#     # print(datapack)
#     rowdata = datapack["rowdata"]
#     htmdata = datapack["html"]
#     # print(f'rowdata={rowdata}')
#     # print(f'htmdata={htmdata}')
#     lhref = rowdata["href"]
#     # print(lhref)
#     eurl = url + lhref
#     print(eurl)
#     title = rowdata["title"]
#     ftitle = '{0:04}'.format(curridx) + '-' + title
#     print(ftitle)
#     contenttxt = getPageData(eurl)
#     print(contenttxt)


def getPageHTMLdata(eurl):
    response = rq.get(eurl)  # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text  # text 屬性就是 html 檔案
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.prettify())  # 把排版後的 html 印出來


def getChapListData(bschapList):
    lst = []
    for item in bschapList:
        adata = item.find("a", href=True)
        # print(adata)
        if adata is not None:
            href = adata['href']
            title = adata['title']
            data = {
                "href": href,
                "title": title
            }
            lst.insert(0, data)
            # print(data)
    # print(lst)
    return lst


def getOneChapData(url, idx, lst):
    # 56287.html 第一章
    # url = "https://tw.uukanshu.com"
    # print(type(resultlst))

    curridx = idx - 1
    # print(f'curridx={curridx}')
    dicdata = lst[curridx]
    # print(dicdata)
    # datapack = dicdata[1]
    # # print(datapack)
    # rowdata = datapack["rowdata"]
    # htmdata = datapack["html"]
    # # print(f'rowdata={rowdata}')
    # # print(f'htmdata={htmdata}')
    lhref = dicdata["href"]
    # print(lhref)
    ltitle = dicdata["title"]
    msg = f"{curridx}---{ltitle}"
    print(msg)
    # print(f"{lhref}--{ltitle}")
    eurl = url + lhref
    # print(eurl)
    contenttxt = getPageData(eurl)
    print(contenttxt)


def demo_get_twuuweb():
    #mid = '33'
    mid = '76656'
    #print(f'word = {word}')
    # https://t.uukanshu.com/book.aspx?id=5199
    url = f"https://tw.uukanshu.com"
    url_b = f"{url}/b/{mid}/"  # PTT NBA 板
    response = rq.get(url_b)  # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text  # text 屬性就是 html 檔案
    soup = BeautifulSoup(response.text, "html.parser")  # 指定 lxml 作為解析器
    # print(soup.prettify())  # 把排版後的 html 印出來
    bschapList = soup.find("ul", attrs={"id": "chapterList"}).find_all("li")
    # cls()
    lst = getChapListData(bschapList)
    # print(lst)
    chap = 4624
    cls()
    print("*****************************")
    print("*****************************")

    getOneChapData(url, chap, lst)
    print("-----------------------------")
    print("-----------------------------")

    return
# ===========================================================


def getuuPageData(eurl):
    # print(url)
    textstr = ""
    response = rq.get(eurl)  # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text  # text 屬性就是 html 檔案
    bpage = BeautifulSoup(response.text, "html.parser")
    # print(bpage.prettify())  # 把排版後的 html 印出來
    pcontent = bpage.find("p", {"class": "readcotent"})
    # print(pcontent.prettify())
    textstr = pcontent.getText()
    print(textstr)
    # print(simplified2Traditional(textstr))
    print("\n")


def getuuneChapData(url, idx, lst):
    curridx = idx - 1
    # print(f'curridx={curridx}')
    dicdata = lst[curridx]
    # print(dicdata)
    # datapack = dicdata[1]
    lhref = dicdata["href"]
    # print(lhref)
    ltitle = dicdata["title"]
    msg = f"{curridx}---{ltitle}"
    print(msg)
    # print(f"{lhref}--{ltitle}")
    eurl = url + lhref
    # print(eurl)
    getuuPageData(eurl)


def getuuChapList(bschapList):
    lst = []
    for item in bschapList:
        adata = item.find("a", href=True)
        if adata is not None:
            # print(adata)
            # print(adata.text)
            title = adata.text
            href = adata['href']
            data = {
                "href": href,
                "title": title
            }
            lst.append(data)
    # print(lst)
    return lst


def demo_get_uuweb():
    # https://uukanshu.cc/book/6750/

    # ------
    mid = '5600'
    chap = 1750
    # ------
    # ------
    # mid = '5316'
    # chap = 44
    # ------
    url = f"https://uukanshu.cc"
    url_b = f"{url}/book/{mid}/"
    response = rq.get(url_b)  # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text  # text 屬性就是 html 檔案
    soup = BeautifulSoup(response.text, "html.parser")  # 指定 lxml 作為解析器
    # print(soup.prettify())  # 把排版後的 html 印出來
    cls()
    bschapList = soup.find("div", attrs={"id": "list-chapterAll"}).find_all("dd")
    # print(bschapList)
    lst = getuuChapList(bschapList)
    # print(lst)
    # chap = 44

    print("*****************************")
    print("*****************************")
    getuuneChapData(url, chap, lst)
    print("-----------------------------")
    print("-----------------------------")


def demo_get_mtwuuweb():
    mid = '5199'
    #print(f'word = {word}')
    # https://t.uukanshu.com/book.aspx?id=5199
    url = f"https://t.uukanshu.com/book.aspx?id={mid}"
    response = rq.get(url)  # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text  # text 屬性就是 html 檔案
    soup = BeautifulSoup(response.text, "html.parser")  # 指定 lxml 作為解析器
    # print(soup.prettify())  # 把排版後的 html 印出來
    lst = soup.find("ul", attrs={"id": "chapterList"}).find_all("li")
    print(lst)


if __name__ == '__main__':
    demo_get_uuweb()
    # demo_get_twuuweb()
    # demo_get_mtwuuweb()

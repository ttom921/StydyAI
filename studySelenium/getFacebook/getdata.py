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
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains

import requests as rq
from bs4 import BeautifulSoup


@contextmanager
def make_chromw_driver() -> Chrome:
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--start-maximized")
    options.add_argument("--auto-open-devtools-for-tabs")
    options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")
    # options.add_argument(f"Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1")
    driver = Chrome(ChromeDriverManager().install(), options=options)
    yield driver
    driver.quit()


def demo_facebook_data():
    with make_chromw_driver() as driver:
        driver.get("https://m.facebook.com/people/%E6%AF%8F%E6%97%A5%E7%82%BA%E5%AD%A9%E5%AD%90%E7%A6%B1%E5%91%8A/100078089262603/")
        time.sleep(5)
        # perform the operation
        # actions = ActionChains(driver)
        # actions.send_keys(Keys.LEFT_CONTROL, Keys.SHIFT, "M")
        # actions.perform()

        ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys('m').perform()

        time.sleep(5)

        # driver.get("https://m.facebook.com/people/%E6%AF%8F%E6%97%A5%E7%82%BA%E5%AD%A9%E5%AD%90%E7%A6%B1%E5%91%8A/100078089262603/")
        # time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # 取得要如何拿到class
        # print(soup.prettify())
        results = soup.find_all("div", dir="auto")
        print(results)
        all_results = soup.find_all("div", class_="native-text")
        print(all_results)
        return

        idx = 0
        for content in all_results:
            if idx == 1:
                print(content.text)
            idx += 1

        # facebookclass = "x11i5rnm xat24cr x1mh8g0r x1vvkbs xdj266r x126k92a"
        # facebookclass = "x11i5rnm xat24cr x1mh8g0r x1vvkbs xtlvy1s x126k92a"
        # titles = soup.find_all("div", class_=facebookclass)
        # print(titles)
        # for i in enumerate(titles):
        #     if i == 1:
        #         print(i, titles[i].text)
        # for title in titles:
        #     # print(title.select_one("div"))
        #     result = title.select_one("div")
        #     print(result.text)


def getPageData(url):
    # print(url)
    response = rq.get(url)  # 用 requests 的 get 方法把網頁抓下來
    html_doc = response.text  # text 屬性就是 html 檔案
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("div", dir="auto")
    print(results)


if __name__ == '__main__':
    # url = "https://www.facebook.com/people/%E6%AF%8F%E6%97%A5%E7%82%BA%E5%AD%A9%E5%AD%90%E7%A6%B1%E5%91%8A/100078089262603/"
    # getPageData(url)
    demo_facebook_data()

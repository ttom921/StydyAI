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

from bs4 import BeautifulSoup


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


if __name__ == '__main__':
    demo_facebook_data()

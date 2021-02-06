from selenium import webdriver
from module.utils import check_response, get_data, pathway_to_third_page
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from module.all_flow import select_1by1, third_page_test, select_4orMore, app_iscsi_test, select_2by2
import os
import time
import asyncio


def main():
    start = time.time()
    # driver
    durl = "./chromedriver"
    driver = webdriver.Chrome(durl)

    wait = WebDriverWait(driver, 10)
    url = "https://www.synology.com/zh-tw/support/nas_selector"

    if not check_response(url):
        print("URL not found or Error")
    else:
        driver.get(url)
        # Assume we got data from database or api
        selection = get_data()
        # # Select 1 by 1 and check the workflow of the 1-3 page is functionable

        # first page click more than 3:
        # page_1_4orMore=select_4orMore(driver, selection)
        # print("Page 1 selected more than 4 app disable? ",page_1_4orMore)
        # Select 1 by 1
        # page_1, page_2 = select_1by1(driver, selection)
        # print("Page 1 functionable? ", page_1)
        # print("Page 2 functionable? ", page_2)
        # time.sleep(3)
        # driver.refresh()
        # Select 2 by 2
        res_2by2 = select_2by2(driver, selection)
        print("Select 2 by 2:", res_2by2)
        # app_iscsi_test(driver, selection)

        # Third page Test
        # page_3 = third_page_test(driver)
        # print("Page 3 functionable? ", page_3)

    driver.close()
    print("elapsed time:", time.time()-start)


if __name__ == "__main__":
    main()

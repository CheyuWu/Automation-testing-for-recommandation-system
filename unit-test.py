from selenium import webdriver
from module.utils import check_response
from module import select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time
import asyncio

def main():
    driver = webdriver.Chrome()

    wait = WebDriverWait(driver, 10)
    url = "https://www.synology.com/zh-tw/support/nas_selector"

    if not check_response(url):
        print("URL not found or Error")
    else:
        driver.get(url)

    selection = {
        "user_type_business": {},
        "user_type_home": {},
    }
    # collect options
    driver.find_element(By.XPATH, "//label[@for='user_type_business']").click()

    business = driver.find_elements_by_xpath(
        "//label[starts-with(@for,'app_')]")
    for i in business:
        selection['user_type_business'][i.get_attribute('for')] = dict()

    driver.find_element_by_css_selector("input#user_type_home").click()
    home = driver.find_elements_by_xpath("//label[starts-with(@for,'app_')]")

    # driver.find_element(By.XPATH, "//input[@id='app_fileserver']").click()
    for i in home:
        selection['user_type_home'][i.get_attribute('for')] = dict()

    ## iterate all function in first page
    # select1 = select.select_1by1(driver, selection)
    # print(select1)
    select2 = select.select_2by2(driver, selection)
    print(select2)

    # time.sleep(10)
    # driver.close()


if __name__ == "__main__":
    main()

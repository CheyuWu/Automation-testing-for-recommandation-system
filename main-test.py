from selenium import webdriver
from module.utils import check_response
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
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
        "user_type_home": {

        },
        "user_type_business": {

        },
    }
    # driver.find_element(By.XPATH, "//label[@for='user_type_business']").click()

    driver.find_element_by_css_selector("input#user_type_home").click()

    driver.find_element(By.XPATH, "//input[@id='app_fileserver']").click()

    time.sleep(20)


if __name__ == "__main__":
    main()

from selenium import webdriver
from module.utils import check_response, get_data
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import asyncio


def main():
    # when using mac
    durl = "./chromedriver"
    driver = webdriver.Chrome(durl)

    wait = WebDriverWait(driver, 10)
    url = "https://www.synology.com/zh-tw/support/nas_selector"

    if not check_response(url):
        print("URL not found or Error")
    else:
        driver.get(url)
    
    ## Assume we get data from database or api
    selection = get_data()

    for user_type, btn in selection.items():
        driver.find_element(By.XPATH, "//label[@for="+"'"+str(user_type)+"'"+"]").click()
        for cond, opt in btn.items():
            print(cond,)
            for idx, lst in opt.items():
                print(idx)
                print(lst)
                break
            break
        break
        # selection['user_type_home'][str(idx)] = []
        # # print("idx: ",idx)
        # driver.find_element(
        #     By.XPATH, "//input[@id="+"'"+str(idx)+"'"+"]").click()

        # # Click "next" button
        # element = driver.find_element_by_css_selector("button.margin_bottom30")
        # driver.execute_script("arguments[0].click()", element)

        # element2 = driver.find_elements_by_class_name("nas_s_lab")
        # for i in element2:
        #     print("for : ", i.get_attribute('for'))
        #     element_sub = driver.find_element_by_id(i.get_attribute('for'))
        #     print("name : ", element_sub.get_attribute("name"))
        # # collect all types of requirement
        # # driver.find_elements_by_xpath("//label[starts-with(@for,'app_')]")
        # # for sub_idx, sub_value in selection['user_type_home'][str(idx)].items():
        # #     selection['user_type_home'][str(idx)].append(str(sub_idx))

        # break

    time.sleep(3)
    driver.close()


if __name__ == "__main__":
    main()

from selenium import webdriver
from module.utils import check_response, get_data, pathway_to_third_page
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from module.all_flow import (select_1by1, third_page_test, select_4orMore, app_iscsi_test,
                             select_2by2, select_3by3, unclick_app)
import os
import time
import asyncio
import pandas as pd


def main():
    log_data = dict()
    start = time.time()
    tmp = time.time()
    # driver
    durl = "./chromedriver"
    driver = webdriver.Chrome(durl)

    wait = WebDriverWait(driver, 10)
    url = "https://www.synology.com/zh-tw/support/nas_selector"
    log_data["Connection_Test"]=dict()
    if not check_response(url):
        # Store the Log DATA
        log_data["Connection_Test"]["Status"] = False
        log_data["Connection_Test"]["Elapsed_Time"] = time.time()-tmp
        tmp = time.time()
        print("URL not found or Error")
    else:
        driver.get(url)
        # Store the Log DATA
        log_data["Connection_Test"]["Status"] = True
        log_data["Connection_Test"]["Elapsed_Time"] = time.time()-tmp

        # Assume we got data from database or api
        selection = get_data()
        # Select 1 by 1 and check the workflow of the 1-3 page is functionable
        page_1, page_2, page_3 = select_1by1(driver, selection)
        # Page Workflow Test
        # Store the Log DATA
        log_data["Page_1_to_Page_2"]=dict()
        log_data["Page_2_to_Page_3"]=dict()
        log_data["Page_3_to_Page_1"]=dict()
        log_data["Page_1_to_Page_2"]["Status"] = page_1
        log_data["Page_1_to_Page_2"]["Elapsed_Time"] = time.time()-tmp
        log_data["Page_2_to_Page_3"]["Status"] = page_2
        log_data["Page_2_to_Page_3"]["Elapsed_Time"] = time.time()-tmp
        log_data["Page_3_to_Page_1"]["Status"] = page_3
        log_data["Page_3_to_Page_1"]["Elapsed_Time"] = time.time()-tmp

        print("Page 1 to Page 2 functionable? ", page_1)
        print("Page 2 to Page 3 functionable? ", page_2)
        print("Page 3 to Page 1 functionable? ", page_3)

        tmp = time.time()
        driver.refresh()
        time.sleep(2)

        # Select 2 by 2
        select_2by2_result = select_2by2(driver, selection)
        # Store the Log DATA
        log_data["Select_2_by_2"]=dict()
        log_data["Select_2_by_2"]["Status"] = select_2by2_result
        log_data["Select_2_by_2"]["Elapsed_Time"] = time.time()-tmp
        tmp = time.time()

        print("Select 2 by 2:", select_2by2_result)
        driver.refresh()
        time.sleep(3)

        # Select 3 by 3
        select_3by3_result = select_3by3(driver, selection, 3)
        # Store the Log DATA
        log_data["Select_3_by_3"]=dict()
        log_data["Select_3_by_3"]["Status"] = select_3by3_result
        log_data["Select_3_by_3"]["Elapsed_Time"] = time.time()-tmp
        tmp = time.time()

        print("Select 3 by 3: ", select_3by3_result)
        driver.refresh()
        time.sleep(3)
        # Unit test
        # test app iscsi
        result_app_iscsi_test = app_iscsi_test(driver, selection)
        # Store the Log DATA
        log_data["app_iscsi_test"]=dict()
        log_data["app_iscsi_test"]["Status"] = result_app_iscsi_test
        log_data["app_iscsi_test"]["Elapsed_Time"] = time.time()-tmp
        tmp = time.time()

        print("App ISCSI Test: ", result_app_iscsi_test)
        driver.refresh()
        time.sleep(2)
        # Third page Test
        page_3_test_result = third_page_test(driver)
        # Store the Log DATA
        log_data["third_page_test"]=dict()
        log_data["third_page_test"]["Status"] = page_3_test_result
        log_data["third_page_test"]["Elapsed_Time"] = time.time()-tmp

        print("Page 3 functionable? ", page_3)
        tmp = time.time()
        driver.refresh()
        time.sleep(2)
        # first page click more than 3:
        page_1_selected_4_or_More = select_4orMore(driver, selection)
        # Store the Log DATA
        log_data["page_1_selected_4_or_More"]=dict()
        log_data["page_1_selected_4_or_More"]["Status"] = page_1_selected_4_or_More
        log_data["page_1_selected_4_or_More"]["Elapsed_Time"] = time.time()-tmp

        print("Page 1 selected more than 4 app is disable? ",
              page_1_selected_4_or_More)
        tmp = time.time()
        driver.refresh()
        time.sleep(2)
        # Unclick first page app and back btn is functionable?
        for selected in range(1, 4):
            unclick_app_result = unclick_app(driver, selection, selected)
            # Store the Log DATA
            log_data["Unclick app " +str(selected)+" result(s)"]=dict()
            log_data["Unclick app " +str(selected)+" result(s)"]["Status"] = unclick_app_result
            log_data["Unclick app " +str(selected)+" result(s)"]["Elapsed_Time"] = time.time()-tmp
            tmp = time.time()
            print("Unclick app "+str(selected) +
                  " result(s)? ", unclick_app_result)

    driver.close()
    print("elapsed time:", time.time()-start)

    print(pd.DataFrame(log_data))
    pd.DataFrame(log_data).T.to_csv("./log.csv",encoding="utf_8_sig")

if __name__ == "__main__":
    main()

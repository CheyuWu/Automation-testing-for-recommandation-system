from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
import numpy as np
import os
import time
import itertools


def click_btn(driver, click_lst):
    try:
        # check is a list or not
        if isinstance(click_lst, list):
            for i in click_lst:
                driver.find_element(
                    By.XPATH, "//input[@id="+"'"+str(i)+"'"+"]").click()
        else:
            # try:
                element= driver.find_element(
                By.XPATH, "//input[@id='"+str(click_lst)+"']")#.click()
            # except ElementClickInterceptedException:
            #     driver.find_element(
            #     By.XPATH, "//input[@id='"+str(click_lst)+"']").click()
                driver.execute_script("arguments[0].click()", element)
        return True

    except Exception as ex:
        # do something
        print("click_btn: ", ex)
        # return False

# click the btn in the second pages


def btn_in_second_page(driver):
    try:
        # Click "next" button to the third page
        next_btn = driver.find_element_by_xpath(
            "//button[@class='btn btn-primary blue']")
        driver.execute_script("arguments[0].click()", next_btn)

        # wait until the third page loaded
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='reset_result']"))
        )
        return True

    except Exception as ex:
        # do something
        print("click_first_btn: ", ex)


def btn_in_first_page(driver, condition):
    try:
        # Click the button
        click_result = click_btn(driver, condition)
        # print("condition: ",condition)
        if not click_result:
            # do something
            pass

        # Click "next" button to the second page
        element = driver.find_element_by_css_selector(
            "button.margin_bottom30.btn.btn-primary.blue")
        driver.execute_script("arguments[0].click()", element)
        return True
    except Exception as ex:
        # do something
        print("click_first_btn: ", ex)


def select_1by1(driver, selection):
    actions = ActionChains(driver)
    for user_type, btn in selection.items():
        res = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//label[@for='"+str(user_type)+"']")))
        driver.execute_script("arguments[0].click()", res)

        for cond, options in btn.items():
            click_result = btn_in_first_page(driver, cond)
            print("condition", cond)
            arr = []
            iops_arr = None
            for idx, lst in options.items():
                # iops dealing alone
                if idx == "iops":
                    iops_arr = lst
                    # iops_flag = True
                else:
                    arr.append(lst)
            
            # If there is only IOPS, then we deal with that
            if len(arr) == 0 and iops_arr:

                for i in iops_arr:
                    blank = driver.find_element_by_xpath(
                        "//input[@iops='"+str(i)+"']")
                    blank.clear()
                    blank.send_keys("25")

                second_to_third_result = btn_in_second_page(driver)
                if not second_to_third_result:
                    # do something
                    pass

                # back to previous page
                reset = driver.find_element_by_id("reset_result")
                driver.execute_script("arguments[0].click()", reset)
                ress=WebDriverWait(driver, 10,).until(
                EC.presence_of_element_located((By.XPATH, "//label[@for='"+str(user_type)+"']")))
                driver.execute_script("arguments[0].click()",ress)
                ## Use continue, because we just want to do it once
                continue
            else:
                # get all possible
                all_possible = list(itertools.product(*arr))

            for element in all_possible:
                for sub_elmt in element:
                    radio_btn = driver.find_element_by_id(sub_elmt)

                    driver.execute_script("arguments[0].click()", radio_btn)
                if iops_arr:
                    for i in iops_arr:
                        blank = driver.find_element_by_xpath(
                            "//input[@iops='"+str(i)+"']")
                        blank.clear()
                        blank.send_keys("25")

                second_to_third_result = btn_in_second_page(driver)
                if not second_to_third_result:
                    # do something
                    pass

                reset = driver.find_element_by_id("reset_result")
                driver.execute_script("arguments[0].click()", reset)
                # usr_type=driver.find_element_by_xpath("//label[@for='"+str(user_type)+"']")
                ress=WebDriverWait(driver, 10,).until(
                EC.presence_of_element_located((By.XPATH, "//label[@for='"+str(user_type)+"']")))
                driver.execute_script("arguments[0].click()",ress)
            
                click_result = btn_in_first_page(driver, cond)
            
            element = driver.find_element_by_css_selector("a.btn.page2-buttons-back")
            driver.execute_script("arguments[0].click()", element)
            click_result = click_btn(driver, cond)
            if not click_result:
                # do something
                pass

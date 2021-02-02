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
            driver.find_element(
                By.XPATH, "//input[@id="+"'"+str(click_lst)+"'"+"]").click()
        return True

    except Exception as ex:
        # do something
        print("click_btn: ", ex)
        # return False

# click the btn in the first pages
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

def select_1by1(driver, selection):
    # try:
    for user_type, btn in selection.items():
        for cond, options in btn.items():
            driver.find_element(By.XPATH, "//label[@for='"+str(user_type)+"']").click()
            ## check first pages is functionable
            result_1 = first_page_select(driver, cond)
            result_2 = second_page_select(driver, cond, options)

            # unclick the button
            # click_result = click_btn(driver, cond)
            # if not click_result:
            #     # do something
            #     pass
        # print("all success")

        # driver.find_element(By.XPATH,"//div[@id='reset_result']").click()

            # driver.find_element(By.XPATH, "//label[@for='"+str(user_type)+"']").click()

            # result = first_page_select(driver, list(selection[str(key)].keys())[i])

    # except Exception as ex:
    #     # do something
    #     print("select_1by1: ", ex)
    # return #result

    # return #result


def first_page_select(driver, condition):
    try:
        click_result = btn_in_first_page(driver, condition)
        if not click_result:
            # do something
            pass

        # I don't know it's required or not
        # if the function is working, then return previous pages
        element = driver.find_element_by_css_selector("a.btn.page2-buttons-back")
        driver.execute_script("arguments[0].click()", element)

        # # Click "next" button, back to the second page
        # element = driver.find_element_by_css_selector("button.margin_bottom30.btn.btn-primary.blue")
        # driver.execute_script("arguments[0].click()", element)

        # unclick the button
        click_result = click_btn(driver, condition)
        if not click_result:
            # do something
            pass

    except Exception as ex:
        # do something
        print("first_page_select: ", ex)
        # return False


def second_page_select(driver, condition, options):
    # try:
    # ActionChains
    action_chain = ActionChains(driver)

    print("condition", condition)
    click_result = btn_in_first_page(driver, condition)
    if not click_result:
        # do something
        pass

    arr = []
    count = 0
    iops_arr = None
    # iops_flag=False
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
            blank = driver.find_element_by_xpath("//input[@iops='"+str(i)+"']")
            blank.clear()
            blank.send_keys("25")

        second_to_third_result = btn_in_second_page(driver)
        if not second_to_third_result:
            # do something
            pass

        # back to previous pag
        prev_page = driver.find_element_by_xpath(
            "//i[@class='fa fa-angle-left']")
        driver.execute_script("arguments[0].click()", prev_page)

    else:
        # get all possible
        all_possible = list(itertools.product(*arr))

        for element in all_possible:
            count += 1
            # Click the second page btn
            for sub_elmt in element:
                # try:
                #     driver.find_element_by_id(sub_elmt).click()

                # except ElementClickInterceptedException:
                # If the btn couldn't be clicked, use the following method
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

            # back to previous page
            # To avoid StaleElementReferenceException
            ignored_exceptions = (NoSuchElementException,
                                  StaleElementReferenceException,)
            back_btn = WebDriverWait(driver, 10,).until(
                EC.presence_of_element_located((By.XPATH, "//i[@class='fa fa-angle-left']")))
            back_btn.click()
            action_chain.move_to_element(back_btn).click().perform()

    # Click back to menu pages
    # back to previous page
    # action_chain.move_to_element(driver.find_element_by_xpath(
    #     "//i[@class='fa fa-angle-left']")).click().perform()

    return True

    # except Exception as ex:
    #     # do something
    #     print("condition", condition)
    #     print("second_page_select: ", ex)
    #     # return False


def third_page_(driver):
    try:

        return
    except Exception as ex:

        return

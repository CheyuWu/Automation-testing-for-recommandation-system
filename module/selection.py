from selenium.webdriver.common.by import By
import numpy as np
import os
import time
import itertools

def click_btn(driver, click_lst):
    try:
        # check is a list or not
        if isinstance(click_lst, list):
            for i in click_lst:
                driver.find_element(By.XPATH, "//input[@id="+"'"+str(i)+"'"+"]").click()
        else:
            driver.find_element(By.XPATH, "//input[@id="+"'"+str(click_lst)+"'"+"]").click()

    except Exception as ex:
        # do something
        print("click_btn: ", ex)
        return False

    return True

def select_1by1(driver, selection):
    try:
        for user_type, btn in selection.items():
            driver.find_element(By.XPATH, "//label[@for="+"'"+str(user_type)+"'"+"]").click()
            for cond, options in btn.items():
                ## check first pages is functionable
                result = first_page_select(driver, cond)
                


                # result = first_page_select(driver, list(selection[str(key)].keys())[i])

    except Exception as ex:
        # do something
        print("select_1by1: ", ex)
        return result

    return result

def first_page_select(driver, condition):
    try:
        # Click the button
        click_result = click_btn(driver, condition)
        print("condition: ",condition)
        if not click_result:
            # do something
            pass

        # Click "next" button to the second page
        element = driver.find_element_by_css_selector("button.margin_bottom30.btn.btn-primary.blue")
        driver.execute_script("arguments[0].click()", element)

        ## I don't know it's required or not
        # if the function is working, then return previous pages
        element = driver.find_element_by_css_selector("a.btn.page2-buttons-back")
        driver.execute_script("arguments[0].click()", element)

         # Click "next" button, back to the second page
        element = driver.find_element_by_css_selector("button.margin_bottom30.btn.btn-primary.blue")
        driver.execute_script("arguments[0].click()", element)

        # # unclick the button
        # click_result = click_btn(driver, condition)
        # if not click_result:
        #     # do something
        #     pass


    except Exception as ex:
        # do something
        print("first_page_select: ", ex)
        return False


def second_page_select(driver, options):
    try:
        arr= []
        iops_arr = None
        # iops_flag=False
        for idx, lst in options.items():
            ## iops dealing alone
            if idx == "iops":
                iops_arr = lst
                # iops_flag = True
            else:
                arr.append(lst)
        # get all possible
        all_possible = list(itertools.product(*arr))

        for element in all_possible:

            for sub_elmt in element:
                driver.find_element_by_id(sub_elmt).click()

            if iops_arr:
                for i in iops_arr:
                    blank=driver.find_element_by_xpath("//input[@iops='"+str(i)+"']")
                    blank.clear()
                    blank.send_keys("25")
            # Click "next" button to the third page
            element = driver.find_element_by_css_selector("button.btn.btn-primary.blue")
            driver.execute_script("arguments[0].click()", element)

        return True

    except Exception as ex:
        # do something
        print("second_page_select: ", ex)
        return False


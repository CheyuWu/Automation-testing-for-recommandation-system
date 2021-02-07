from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from module.utils import (click_btn, btn_in_second_page, btn_in_first_page, pathway_to_third_page, third_to_first_page)
import numpy as np
import os
import time
from itertools import permutations
import itertools


def select_1by1(driver, selection):
    try:
        page_1_to_2 = True
        page_2_to_3 = True
        page_3_to_1 = True

        for user_type, btn in selection.items():
            for cond, options in btn.items():
                ## dealing with data
                arr = []
                iops_arr = None
                for idx, lst in options.items():
                    # iops dealing alone
                    if idx == "iops":
                        iops_arr = lst
                    else:
                        arr.append(lst)
                ## Click the user_type button
                user_type_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='"+str(user_type)+"']")))
                driver.execute_script("arguments[0].click()", user_type_btn)
                # If there is only IOPS, then we deal with that
                if len(arr) == 0 and iops_arr:
                    click_result_first_page = btn_in_first_page(driver, cond)
                    if not click_result_first_page:
                        page_1_to_2 = False
                    for i in iops_arr:
                        blank = driver.find_element_by_xpath(
                            "//input[@iops='"+str(i)+"']")
                        blank.clear()
                        blank.send_keys("25")

                    second_to_third_result = btn_in_second_page(driver)
                    if not second_to_third_result:
                        # do something
                        page_2_to_3 = False

                    # third to first page
                    third_to_first_page_result =third_to_first_page(driver, user_type, cond)
                    if not third_to_first_page_result:
                        page_3_to_1 = False
                    continue

                # get all possible
                all_possible = list(itertools.product(*arr))

                for element in all_possible:
                    click_result_first_page = btn_in_first_page(driver, cond)
                    if not click_result_first_page:
                        page_1_to_2 = False
                    for sub_elmt in element:
                        radio_btn = driver.find_element_by_id(sub_elmt)

                        driver.execute_script("arguments[0].click()", radio_btn)

                    second_to_third_result = btn_in_second_page(driver)
                    # If page 2 occur error, then False
                    if not second_to_third_result:
                        page_2_to_3 = False

                    # third to first page
                    third_to_first_page_result =third_to_first_page(driver, user_type, cond)
                    if not third_to_first_page_result:
                        page_3_to_1 = False

        return page_1_to_2, page_2_to_3, page_3_to_1
    except Exception as ex:
        print("select_1by1:", str(ex))
        return False, False, False


def select_2by2(driver, selection):
    try:
        AC = ActionChains(driver)
        wait = WebDriverWait(driver, 10)
        flag = True
        iops_flag = False
        for user_type in selection.keys():
            for i in range(len(selection[str(user_type)])):
                for j in range(i+1, len(selection[str(user_type)])):

                    if i == (len(selection[str(user_type)])-1):
                        break
                    slt = list(selection[str(user_type)].keys())
                    app_arr = [slt[i], slt[j]]
                    # Click the user type: user or business
                    user_btn = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//label[@for='"+str(user_type)+"']")))
                    driver.execute_script("arguments[0].click()", user_btn)
                    result = btn_in_first_page(driver, app_arr)

                    if not result:
                        flag = False

                    # handle options in second page
                    # click the first btn
                    for idx_i, element_i in selection[str(user_type)][slt[i]].items():
                        if idx_i == 'iops':
                            for value_i in element_i:
                                iops_input = driver.find_element_by_xpath(
                                    "//input[@iops='"+str(value_i)+"']")
                                iops_input.clear()
                                iops_input.send_keys(25)

                        else:
                            sub_btn_i = driver.find_element_by_id(
                                str(element_i[0]))
                            driver.execute_script(
                                "arguments[0].click()", sub_btn_i)

                        for idx_j, element_j in selection[str(user_type)][slt[j]].items():
                            if idx_j not in selection[str(user_type)][slt[i]].keys():

                                if idx_j != 'iops':
                                    sub_btn_j = driver.find_element_by_id(
                                        str(element_j[0]))
                                    driver.execute_script(
                                        "arguments[0].click()", sub_btn_j)

                                elif idx_j == 'iops' and (not iops_flag):

                                    for value in element_j:
                                        iops_input = driver.find_element_by_xpath(
                                            "//input[@iops='"+str(value)+"']")
                                        iops_input.clear()
                                        iops_input.send_keys(15)
                                    iops_flag = True
                                    break

                    # Reset iops flag
                    iops_flag = False

                    # Go to third page
                    third_page = btn_in_second_page(driver)
                    if not third_page:
                        flag = False
                    ## Back to first page
                    third_to_first_page_result = third_to_first_page(driver, user_type, app_arr)
                    if not third_to_first_page_result:
                        flag = False

        return flag
    except Exception as ex:
        print("select_2by2:", str(ex))
        return False


def select_3by3(driver, selection, select_amount):
    try:
        wait = WebDriverWait(driver, 10)
        flag = True
        for user_type in selection.keys():
            ## Create all possibilities
            data_list = list(permutations(list(selection[str(user_type)].keys()), select_amount))
            for opts in data_list:
                user_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='"+str(user_type)+"']")))
                driver.execute_script("arguments[0].click()", user_btn)
                first_page_result = btn_in_first_page(driver, list(opts))
                if not first_page_result:
                    flag = False
                ## Store the clicked_btn
                tmp_app_condition = []
                for app in opts:
                    for condition, element in selection[str(user_type)][str(app)].items():
                        if condition not in tmp_app_condition:
                            tmp_app_condition.append(condition)
                            if condition == 'iops':
                                for amount in selection[str(user_type)][str(app)][condition]:
                                    iops_input =driver.find_element_by_xpath("//input[@iops='"+str(amount)+"']")
                                    iops_input.clear()
                                    iops_input.send_keys(25)
                            else :
                                radio_btn = driver.find_element_by_xpath("//input[@id='"+str(element[0])+"']")
                                driver.execute_script("arguments[0].click()", radio_btn)
                ## Second page to third page
                second_to_third_result = btn_in_second_page(driver)
                if not second_to_third_result:
                    flag= False
                
                ## Third page back to first page
                third_to_first_page_result = third_to_first_page(driver, user_type, list(opts))
                if not third_to_first_page_result:
                    flag = False
        return flag
    except Exception as ex:
        print("select_3by3: ",str(ex))
        return False

def third_page_test(driver):
    try:
        # Go to third page
        path_to_3 = pathway_to_third_page(driver)
        if not path_to_3:
            return False

        # Get all tab
        tab = driver.find_elements_by_xpath("//div[@class='bay_txt']")

        for sub_tab in tab:
            driver.execute_script("arguments[0].click()", sub_tab)
            output_prods = driver.find_elements_by_class_name("product_box")

            # it can't be compare, if len is lower than 2
            if len(output_prods) < 2:
                continue
            res = third_page_unclick_test(driver, output_prods)
            if not res:
                return False

            for sub_prod in output_prods:
                try:
                    sub_btn = sub_prod.find_element_by_xpath(
                        "//a[@class='add_to_compare tip']")

                    driver.execute_script("arguments[0].click()", sub_btn)

                except NoSuchElementException:
                    break

            # Click compare button
            compare_btn = driver.find_element_by_xpath(
                "//a[@class='btn btn-xs round btn-primary']")
            driver.execute_script("arguments[0].click()", compare_btn)
            # switch to new tab
            driver.switch_to.window(driver.window_handles[1])
            cp_res = compare_result(driver)
            driver.close()
            if not cp_res:
                # do something
                return cp_res
            driver.switch_to.window(driver.window_handles[0])
            compare_reset = driver.find_element_by_id("compare_toolbar_reset")
            driver.execute_script("arguments[0].click()", compare_reset)

        return True

    except Exception as ex:
        print(str(ex))
        return False


def compare_result(driver):
    try:
        # Click the hightlighted btn
        driver.find_element_by_xpath("//input[@type='checkbox']").click()

        ## not highlighted
        table_data_h = driver.find_elements_by_xpath(
            "//tr[@class='th3 highlight']")
        # highlighted
        table_data = driver.find_elements_by_xpath("//tr[@class='tr3']")

        # hightlight must different
        compare_flag = True
        for row in table_data_h:
            tmp = None
            if not compare_flag:
                break
            for col in row.find_elements_by_tag_name("td")[1:]:
                class_name = col.text
                if class_name == '':
                    class_name = str(col.find_element_by_tag_name(
                        "i").get_attribute('class'))
                if tmp:
                    tmp = class_name
                elif tmp == class_name:
                    compare_flag = False
                    break
        return compare_flag

    except Exception as ex:
        print(str(ex))
        return False


def third_page_unclick_test(driver, output_prods):
    try:
        data_name = None
        for idx in range(len(output_prods)):
            try:
                # print(idx)
                sub_btn = output_prods[idx].find_element_by_xpath(
                    "//a[@class='add_to_compare tip']")
                driver.execute_script("arguments[0].click()", sub_btn)
                # Store the latest data-name
                data_name = sub_btn.get_attribute('data-name')
                # print(data_name)
            except NoSuchElementException:

                # unclick the previous one
                prev_sub_btn = output_prods[idx-1].find_element_by_xpath(
                    "//a[@data-name='"+data_name+"']")
                driver.execute_script("arguments[0].click()", prev_sub_btn)

                # Click the current one
                # The total slot is 5
                sub_btn = output_prods[idx].find_elements_by_xpath(
                    "//a[@class='add_to_compare tip']")[idx-4]
                data_name = sub_btn.get_attribute('data-name')
                driver.execute_script("arguments[0].click()", sub_btn)

        item_arr = driver.find_elements_by_xpath("//a[@class='btn-remove']")
        for element in item_arr:

            driver.execute_script("arguments[0].click()", element)

        return True
    except Exception as ex:
        print(str(ex))
        return False


def select_4orMore(driver, selection):
    try:
        flag = True
        for key, values in selection.items():
            driver.find_element_by_id(str(key)).click()

            for idx, app in enumerate(list(values.keys())):
                app_btn = driver.find_element_by_id(str(app))
                driver.execute_script("arguments[0].click()", app_btn)

                element = driver.find_element_by_css_selector(
                    "button.margin_bottom30")
                # print("disabled: ",element.get_attribute('disabled'))
                if (idx+1) > 3 and not element.get_attribute('disabled'):
                    flag = False

        return flag
    except Exception as ex:
        print(str(ex))
        return False


def app_iscsi_test(driver, selection):
    try:
        flag = True
        for i in selection['user_type_business']['app_iscsi']['iops']:
            user_type = WebDriverWait(driver, 10,).until(
                EC.presence_of_element_located((By.XPATH, "//label[@for='user_type_business']")))
            driver.execute_script("arguments[0].click()", user_type)

            app_btn = driver.find_element_by_id('app_iscsi')
            driver.execute_script("arguments[0].click()", app_btn)

            element = driver.find_element_by_css_selector(
                "button.margin_bottom30")
            driver.execute_script("arguments[0].click()", element)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//input[@iops='"+str(i)+"']"))
            )
            # click next and check if it will go to third page, then False
            # check the sum of vm can equal to 0 ?
            driver.find_element_by_xpath("//button[@class='btn btn-primary blue']").click()
            element = driver.find_element_by_xpath("//label[@class='error_vmm_total']")

            if element.get_attribute('style') != '':
                flag = False
            ## Test if the sum of vm == -1 or 0.1 or >100 or alphabat
            for sum_of_vm in ["A","BCD", 0.1, -1, 200,]:
                blank = driver.find_element_by_xpath("//input[@iops='"+str(i)+"']")
                blank.clear()
                driver.execute_script("arguments[0].value=arguments[1]",blank,'')
                blank.send_keys(str(sum_of_vm))
                input_amount = blank.get_attribute("value")
                ## 
                if input_amount != '':
                    if int(input_amount)<=0 or int(input_amount)>100:
                        driver.find_element_by_xpath("//button[@class='btn btn-primary blue']").click()
                        element = driver.find_element_by_xpath("//label[@class='error_vmm_total']")
                        if element.get_attribute('style') != '':
                            flag = False  
                else :
                    driver.find_element_by_xpath("//button[@class='btn btn-primary blue']").click()
                    element = driver.find_element_by_xpath("//label[@class='error_vmm_total']")

                    if element.get_attribute('style') != '':
                        flag = False
                
                ## back to first page and click next btn to second page (To reset input)
                back_first_btn = driver.find_element_by_css_selector("a.btn.page2-buttons-back")
                driver.execute_script("arguments[0].click()", back_first_btn)
                ## Click "next" button to the second page
                first_to_second_btn = driver.find_element_by_css_selector("button.margin_bottom30.btn.btn-primary.blue")
                driver.execute_script("arguments[0].click()", first_to_second_btn)

            ## Test the normal input
            blank = driver.find_element_by_xpath("//input[@iops='"+str(i)+"']")
            blank.clear()
            blank.send_keys("100")
            driver.find_element_by_xpath("//button[@class='btn btn-primary blue']").click()

            # wait
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@id='reset_result']"))
            )

            reset = driver.find_element_by_id("reset_result")
            driver.execute_script("arguments[0].click()", reset)

        return flag
    except Exception as ex:
        print("app_iscsi_test", str(ex))
        return False

def unclick_app(driver, selection, select_amount):
    try :
        wait = WebDriverWait(driver, 10)
        flag = True
        for user_type in selection.keys():
            ## Create all possibilities
            data_list = list(permutations(list(selection[str(user_type)].keys()), select_amount))
            for opts in data_list:
                user_type_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='"+str(user_type)+"']")))
                driver.execute_script("arguments[0].click()", user_type_btn)
                first_page_result = btn_in_first_page(driver, list(opts))
                if not first_page_result:
                    flag = False

                ## back to first page and unclick app
                back_first_btn = driver.find_element_by_css_selector("a.btn.page2-buttons-back")
                driver.execute_script("arguments[0].click()", back_first_btn)

                ## Unclick button
                unclick_result = click_btn(driver, list(opts))
                if not unclick_result:
                    flag = False
        return flag
    except Exception as ex:
        print("unclick_app: ", str(ex))
        return False
   
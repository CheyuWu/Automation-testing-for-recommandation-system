from selenium.webdriver.common.by import By
# import pandas as pd
import os
import time

def click_btn(driver, click_lst):
    try:
        ## check is a list or not
        if isinstance(click_lst, list): 
            for i in click_lst:
                driver.find_element(By.XPATH, "//input[@id="+"'"+str(i)+"'"+"]").click()
        else :
            driver.find_element(By.XPATH, "//input[@id="+"'"+str(click_lst)+"'"+"]").click()
        
    except Exception as ex:
        # do something
        print("click_btn: ",ex)
        return False

    return True

def first_page_select(driver, name):
    try:
        # selection[str(key)][str(idx)] = []

        ## Click the button
        click_result = click_btn(driver, name)

        if not click_result:
            # do something
            pass

        ## Click "next" button
        element = driver.find_element_by_css_selector("button.margin_bottom30.btn.btn-primary.blue")
        driver.execute_script("arguments[0].click()", element)
        
        ### if the function is working, then return previous pages
        element = driver.find_element_by_css_selector("a.btn.page2-buttons-back")
        driver.execute_script("arguments[0].click()", element)
        ## unclick the button
        click_result = click_btn(driver, name)
        if not click_result:
            # do something
            pass
        # driver.find_element(By.XPATH, "//input[@id="+"'"+str(name)+"'"+"]").click()

    except Exception as ex:
        # do something
        print("first_page_select: ",ex)
        return False

    return True

def select_1by1(driver, selection):
    try:
        for key in selection.keys():
            driver.find_element(By.XPATH, "//label[@for="+"'"+str(key)+"'"+"]").click()
            for i in range(len(selection[str(key)])):
                result = first_page_select(driver, list(selection[str(key)].keys())[i])
        
    except Exception as ex:
        # do something
        print("select_1by1: ",ex)
        return result
    
    return result


def select_2by2(driver, selection):
    try:
        for key in selection.keys():
            driver.find_element(By.XPATH, "//label[@for="+"'"+str(key)+"'"+"]").click()
            
            for i in range(len(selection[str(key)])):
                
                for j in range(i+1, len(selection[str(key)])):
                    
                    ## if i is the last idx
                    if i == (len(selection[str(key)])-1):
                        break
                    else :
                        slt=list(selection[str(key)].keys())
                        arr = [slt[i],slt[j]]
                    result = first_page_select(driver, arr)

    except Exception as ex:
        # do something
        print("select_2by2: ",ex)
        return result
    return result


def select_3by3(driver, selection):
    try:
        for key in selection.keys():
            driver.find_element(By.XPATH, "//label[@for="+"'"+str(key)+"'"+"]").click()
            
            for i in range(len(selection[str(key)])):
                
                for j in range(i+1, len(selection[str(key)])):
                    ## if i is the last idx
                    if i == (len(selection[str(key)])-1):
                            break
                    else :
                        for k in range(j+1, len(selection[str(key)])):
                            ## if j is the last idx
                            if j == (len(selection[str(key)])-1):
                                break
                            else :
                                slt=list(selection[str(key)].keys())
                                arr = [slt[i],slt[j],slt[k]]
                            result = first_page_select(driver, arr)


    except Exception as ex:
        # do something
        print("select_3by3: ",ex)
        return result
    return result


def select_more_3(driver, selection):
    for key in selection.keys():
        driver.find_element(By.XPATH, "//label[@for="+"'"+str(key)+"'"+"]").click()

        



    return

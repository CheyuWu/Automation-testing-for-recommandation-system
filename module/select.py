from selenium.webdriver.common.by import By
import os


def select_1(driver, selection, start):
    driver.find_element(By.XPATH, "//label[@for="+start+"]").click()
    
    return

def select_2(driver, selection):
    return

def select_3(driver, selection):
    return

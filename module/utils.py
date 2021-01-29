from requests import get
from selenium.webdriver.common.by import By


def check_response(url):
    try:
        request = get(url)
        if not request.status_code == 200:
            return False
        return True
    except Exception as ex:
        return str(ex)


def driver_out(driver):
    try:
        driver.close()
        return True
    except Exception as ex:
        return str(ex)

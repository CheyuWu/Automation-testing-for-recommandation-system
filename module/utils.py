from requests import get
from selenium.webdriver.common.by import By

def check_response(url):
    request=get(url)
    if not request.status_code == 200:
        return False
    return True


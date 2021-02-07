from requests import get
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
def check_response(url):
    try:
        request = get(url)
        if not request.status_code == 200:
            return False
        return True
    except Exception as ex:
        print("check_response:",str(ex))
        return False


def get_data():
    selection = {
        "user_type_business": {
            "app_fileserver": {
                "how_many_devices": [
                    "how_many_devices_checkbox_devices_less_than_20",
                    "how_many_devices_checkbox_devices_less",
                    "how_many_devices_checkbox_devices_medium",
                    "how_many_devices_checkbox_devices_large",
                ],
                "how_many_connection": [
                    "how_many_connection_checkbox_connection_less_than_100",
                    "how_many_connection_checkbox_connection_less",
                    "how_many_connection_checkbox_connection_medium",
                    "how_many_connection_checkbox_connection_large",
                    "how_many_connection_checkbox_connection_large_than_1000",
                ],
                "how_many_throughput": [
                    "how_many_throughput_checkbox_throughput_less_than_120",
                    "how_many_throughput_checkbox_throughput_less",
                    "how_many_throughput_checkbox_throughput_medium",

                ],
            },
            "app_databackup": {
                "how_many_devices": [
                    "how_many_devices_checkbox_devices_less_than_20",
                    "how_many_devices_checkbox_devices_less",
                    "how_many_devices_checkbox_devices_medium",
                    "how_many_devices_checkbox_devices_large",
                ],
                "how_many_connection": [
                    "how_many_connection_checkbox_connection_less_than_100",
                    "how_many_connection_checkbox_connection_less",
                    "how_many_connection_checkbox_connection_medium",
                    "how_many_connection_checkbox_connection_large",
                    "how_many_connection_checkbox_connection_large_than_1000",
                ],
                "how_many_throughput": [
                    "how_many_throughput_checkbox_throughput_less_than_120",
                    "how_many_throughput_checkbox_throughput_less",
                    "how_many_throughput_checkbox_throughput_medium",

                ],
            },
            "app_iscsi": {
                "iops": [70, 150, 500, 2000],
            },
            "app_collatboration": {
                "how_many_devices": [
                    "how_many_devices_checkbox_devices_less_than_20",
                    "how_many_devices_checkbox_devices_less",
                    "how_many_devices_checkbox_devices_medium",
                    "how_many_devices_checkbox_devices_large",
                    "how_many_devices_checkbox_devices_large"
                ],
            },
            "app_mailserver": {
                "how_many_mail_accounts": [
                    "how_many_mail_accounts_checkbox_mail_accounts_less",
                    "how_many_mail_accounts_checkbox_mail_accounts_medium",
                    "how_many_mail_accounts_checkbox_mail_accounts_large",
                ],
            },
            "app_vmm": {
                "how_many_virtual_machines_for_business": [
                    "how_many_virtual_machines_for_business_checkbox_vmm_less",
                    "how_many_virtual_machines_for_business_checkbox_vmm_medium",
                    "how_many_virtual_machines_for_business_checkbox_vmm_large",
                ]
            },

        },
        "user_type_home": {
            "app_fileserver": {
                "how_many_people":
                ["how_many_people_checkbox_people_less",
                 "how_many_people_checkbox_people_medium", "how_many_people_checkbox_people_large"]
            },
            "app_databackup": {
                "how_many_people":
                ["how_many_people_checkbox_people_less",
                 "how_many_people_checkbox_people_medium", "how_many_people_checkbox_people_large"]},

            "app_multimedia": {
                "need_image_recognition":
                ["need_image_recognition_checkbox_no_image_reco",
                 "need_image_recognition_checkbox_yes_image_reco"]},

            "app_productivity": {
                "how_many_people": [
                    "how_many_people_checkbox_people_large", "how_many_people_checkbox_people_medium", "how_many_people_checkbox_people_less"
                ]},

            "app_vmm": {
                "how_many_virtual_machines_for_home": [
                    "how_many_virtual_machines_for_home_checkbox_vmm_less", "how_many_virtual_machines_for_home_checkbox_vmm_medium"
                ]},
        },
    }
    return selection


def pathway_to_third_page(driver):

    try:
        element = driver.find_element_by_xpath("//input[@id='user_type_home']")
        driver.execute_script("arguments[0].click()", element)

        element = driver.find_element(
            By.XPATH, "//input[@id='app_fileserver']")
        driver.execute_script("arguments[0].click()", element)

        # Click "next" button
        element = driver.find_element_by_css_selector("button.margin_bottom30")
        driver.execute_script("arguments[0].click()", element)

        driver.find_element_by_id(
            "how_many_people_checkbox_people_medium").click()
        next_btn = driver.find_element_by_xpath(
            "//button[@class='btn btn-primary blue']")
        driver.execute_script("arguments[0].click()", next_btn)

        # wait until the third page loaded
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='reset_result']"))
        )
        return True
    except Exception as ex:
        print("pathway_to_third_page: ", str(ex))
        return False


def btn_in_first_page(driver, condition):
    try:
        # Click the button
        click_result = click_btn(driver, condition)
        if not click_result:
            # do something
            return False

        # Click "next" button to the second page
        element = driver.find_element_by_css_selector(
            "button.margin_bottom30.btn.btn-primary.blue")

        driver.execute_script("arguments[0].click()", element)

        return True
    except Exception as ex:
        # do something
        print("btn_in_first_page: ", str(ex))
        return False

# click the btn in the second pages

def btn_in_second_page(driver):
    try:
        # Click "next" button to the third page
        next_btn = driver.find_element_by_xpath(
            "//button[@class='btn btn-primary blue']")
        driver.execute_script("arguments[0].click()", next_btn)

        # wait until the third page loaded
        WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//div[@id='reset_result']"))
        )
        return True
    except TimeoutException:
        ## if I enter the strange value it will nothing output
        print("btn_in_second_page: ", "TimeoutException, No items output")
        return True
    except Exception as ex:
        # do something
        print("btn_in_second_page: ", str(ex))
        return False


def click_btn(driver, click_lst):
    try:
        # check is a list or not
        if isinstance(click_lst, list):
            for i in click_lst:
                element = driver.find_element(By.XPATH, "//input[@id="+"'"+str(i)+"'"+"]")
                driver.execute_script("arguments[0].click()", element)
        else:
            element = driver.find_element(
                By.XPATH, "//input[@id='"+str(click_lst)+"']")
            driver.execute_script("arguments[0].click()", element)

        return True

    except Exception as ex:
        # do something
        print("click_btn: ", str(ex))
        return False


def third_to_first_page(driver, user_type, unclick_app = None):
    try:
        flag = True
        AC = ActionChains(driver)
        ## Back to first page
        reset = driver.find_element_by_id("reset_result")
        driver.execute_script("arguments[0].click()", reset)
        ## Click the user_type
        user_type_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='"+str(user_type)+"']")))
        driver.execute_script("arguments[0].click()", user_type_btn)

        return flag

    except NoSuchElementException:
        back_btn = driver.find_element_by_xpath("//i[@class='fa fa-angle-left']")
        ## Click twice and back to first page
        AC.move_to_element(back_btn).double_click().perform()
        #WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='"+str(user_type)+"']")))
        click_result = click_btn(driver, unclick_app)
        if not click_result:
            # do something
            flag = False
        return flag
    except Exception as ex:
        print("third_to_first_page: ",str(ex))
        return False

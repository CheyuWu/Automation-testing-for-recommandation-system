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
                "how_many_people": ["how_many_people_checkbox_people_less",
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

from PyKIPass.URLs import URLs
from PyKIPass.exceptions import *
import requests
import uuid
from datetime import datetime


class KIPass:
    class User:
        boss_name = ""
        is_enabled = ""
        address_detail = ""
        is_transferred = ""
        is_async = ""
        version = ""
        is_boss = ""
        biz_no_count = -1
        authed_phone_number = ""
        phone_number = ""
        business_register_number = ""
        username = ""
        os_type = ""
        business_name = ""
        new_terms_yn = ""
        name = ""
        str_use_yn = "",
        process_type = "",
        business_id = ""
        address = "",
        uuid = "",
        business_type = ""

    class CustomerCountOnDay:
        total_customer_count = -1
        vaccinated_customer_count = -1
        fully_vaccinated_customer_count = -1
        dates = ""
        time = ""

    class CustomerCountOnTwoWeek:
        total_customer_count = -1
        vaccinated_customer_count = -1
        fully_vaccinated_customer_count = -1
        dates = ""

    class VerifyQR:
        voice = ""
        msg = ""
        vaccine_type = ""
        vaccine_code = ""
        background_color = ""
        success = ""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.urls = URLs()
        self.user = self.User()

        # Authentication
        payload = {
            "usr_id": self.username,
            "passwd": self.password,
            "run_version": "1.3.0",
            "os_type": "iOS",
            "udid": str(uuid.uuid4()).upper()
        }

        req = requests.post(url=self.urls.login_url(), json=payload)

        json_data = req.json()

        # Exception handling
        if not req.ok:
            raise RequestIsNotOkay

        if not json_data.get("success"):
            raise ResponseIsNotSuccess(f"Request is not okay: {json_data.get('msg')}")

        if not json_data.get("data"):
            raise ResponseIsNotSuccess(f"Response is not success: {json_data.get('msg')}")

        data = json_data.get("data")

        self.auth = req.headers.get("Authorization")

        self.user.boss_name = data["boss_nm"]
        self.user.is_enabled = data["use_yn"]
        self.user.address_detail = data["addr_detail"]
        self.user.is_transferred = data["transfer_yn"]
        self.user.is_async = data["async_yn"]
        self.user.version = data["run_version"]
        self.user.is_boss = data["boss_yn"]
        self.user.biz_no_count = data["biz_no_count"]
        self.user.authed_phone_number = data["auth_hp_no"]
        self.user.phone_number = data["hp_no"]
        self.user.business_register_number = data["biz_no"]
        self.user.username = data["usr_id"]
        self.user.os_type = data["os_type"]
        self.user.business_name = data["str_nm"]
        self.user.new_terms_yn = data["new_terms_yn"]
        self.user.name = data["usr_nm"]
        self.user.str_use_yn = data["str_use_yn"]
        self.user.process_type = data["process_type"]
        self.user.business_id = data["str_id"]
        self.user.address = data["addr"]
        self.user.uuid = data["udid"]
        self.user.business_type = data["industry_text"]

    def __get_data(self, url, json):
        headers = {"Authorization": self.auth}
        req = requests.post(url=url, json=json, headers=headers)

        json_data = req.json()

        # Exception handling
        if not req.ok:
            raise RequestIsNotOkay

        if not json_data.get("success"):
            raise ResponseIsNotSuccess(f"Request is not okay: {json_data.get('msg')}")

        if not json_data.get("data"):
            raise ResponseIsNotSuccess(f"Response is not success: {json_data.get('msg')}")

        return json_data

    def get_customer_count_on_day(self, date):
        payload = {
            "dates": date,
            "str_id": self.user.uuid
        }

        json_data = self.__get_data(url=self.urls.customer_count_on_day_url(), json=payload)

        customer_count_on_day_list = []

        for data in json_data["data"]:
            customer_count_on_day = self.CustomerCountOnDay()

            customer_count_on_day.total_customer_count = data["pass_count"]
            customer_count_on_day.vaccinated_customer_count = data["inc_count"]
            customer_count_on_day.fully_vaccinated_customer_count = data["inc_comp_count"]
            customer_count_on_day.dates = data["dates"]
            customer_count_on_day.time = data["time"]

            customer_count_on_day_list.append(customer_count_on_day)

        return customer_count_on_day_list

    def get_customer_count_on_two_week(self, start_date, end_date):
        payload = {
            "fdate": start_date,
            "str_id": self.user.uuid,
            "tdate": end_date
        }

        json_data = self.__get_data(url=self.urls.customer_count_on_two_week_url(), json=payload)

        customer_count_on_two_week_list = []

        for data in json_data["data"]:
            customer_count_on_two_week = self.CustomerCountOnTwoWeek()

            customer_count_on_two_week.total_customer_count = data["pass_count"]
            customer_count_on_two_week.vaccinated_customer_count = data["inc_count"]
            customer_count_on_two_week.fully_vaccinated_customer_count = data["inc_comp_count"]
            customer_count_on_two_week.dates = data["dates"]

            customer_count_on_two_week_list.append(customer_count_on_two_week)

        return customer_count_on_two_week_list

    def verify_qr(self, parsed_qr_code):
        date = datetime.now().strftime("%Y%m%d%H%M%S")

        payload = {
            "dates": date,
            "qr_cd": parsed_qr_code,
            "str_id": self.user.business_id,
            "udid": self.user.uuid,
            "usr_id": self.user.username,
            "version": "001"
        }

        json_data = self.__get_data(url=self.urls.verify_qr_url(), json=payload)

        verifyqr = self.VerifyQR()

        verifyqr.voice = json_data["voice"]
        verifyqr.msg = json_data["msg"]
        verifyqr.vaccine_code = json_data.get("inc_code")
        verifyqr.success = json_data["success"]
        verifyqr.vaccine_type = json_data["inc_type"]
        verifyqr.background_color = json_data["background"]

        return verifyqr

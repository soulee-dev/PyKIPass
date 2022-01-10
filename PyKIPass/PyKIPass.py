from PyKIPass.URLs import URLs
from PyKIPass.exceptions import *
import requests
import uuid
from datetime import datetime


class KIPass:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.urls = URLs()

        # Authentication
        self.auth = None
        self.uuid = str(uuid.uuid4()).upper()

    def __login(self):

        if not self.auth:
            payload = {
                "usr_id": self.username,
                "passwd": self.password,
                "run_version": "1.3.0",
                "os_type": "iOS",
                "udid": self.uuid
            }

            r = requests.post(url=self.urls.login_url(), json=payload)
            self.auth = r.headers.get("Authorization")
            self.business_id = r.json()["data"]["str_id"]

    def __get_data(self, url, json):
        self.__login()
        headers = {"Authorization": self.auth}
        req = requests.post(url=url, json=json, headers=headers)

        json_data = req.json()

        # Exception handling
        if not req.ok:
            raise RequestIsNotOkay

        if not json_data.get("success"):
            raise ResponseIsNotSuccess

        if not json_data.get("data"):
            raise ResponseIsNotSuccess

        return json_data

    def get_customer_count_on_day(self, date):
        payload = {
            "dates": date,
            "str_id": self.uuid
        }

        return self.__get_data(url=self.urls.customer_count_on_day_url(), json=payload)

    def get_customer_count_on_two_week(self, start_date, end_date):
        payload = {
            "fdate": start_date,
            "str_id": self.uuid,
            "tdate": end_date
        }

        return self.__get_data(url=self.urls.customer_count_on_two_week_url(), json=payload)

    def verify_qr(self, parsed_qr_code):
        self.__login()
        date = datetime.now().strftime("%Y%m%d%H%M%S")

        payload = {
            "dates": date,
            "qr_cd": parsed_qr_code,
            "str_id": self.business_id,
            "udid": self.uuid,
            "usr_id": self.username,
            "version": "001"
        }

        return self.__get_data(url=self.urls.verify_qr_url(), json=payload)

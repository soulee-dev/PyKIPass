import unittest
import os
from PyKIPass import *
from PyKIPass.exceptions import *


class PyKIPassTest(unittest.TestCase):
    def setUp(self):
        print(os.environ.get("KI_PASS_ID"), os.environ.get("KI_PASS_PASSWORD"))

        self.KIPass = KIPass(username=os.environ.get("KI_PASS_ID"), password=os.environ.get("KI_PASS_PASSWORD"))

    def test_exception_login(self):
        with self.assertRaises(ResponseIsNotSuccess):
            KIPass(username="", password="")

    def test_get_customer_count_on_day(self):
        self.assertTrue(self.KIPass.get_customer_count_on_day(date="20220107")[0].total_customer_count >= 0)

    def test_exception_get_customer_count_on_day(self):
        with self.assertRaises(ResponseIsNotSuccess):
            self.KIPass.get_customer_count_on_day(date="")

    def test_get_customer_count_on_two_week(self):
        self.assertTrue(self.KIPass.get_customer_count_on_two_week(start_date="20211219", end_date="20220102")[0].total_customer_count >= 0)

    def test_exception_verify_qr(self):
        with self.assertRaises(ResponseIsNotSuccess):
            self.KIPass.verify_qr(parsed_qr_code="test_string")


if __name__ == "__main__":
    unittest.main()


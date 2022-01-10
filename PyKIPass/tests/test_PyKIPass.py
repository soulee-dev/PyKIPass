import unittest
import os
from PyKIPass import PyKIPass
from PyKIPass.exceptions import *


class PyKIPassTest(unittest.TestCase):
    def setUp(self):
        print(os.environ.get("KI_PASS_ID"), os.environ.get("KI_PASS_PASSWORD"))

        self.KIPass = PyKIPass.KIPass(os.environ.get("KI_PASS_ID"), os.environ.get("KI_PASS_PASSWORD"))

    def test_get_customer_count_on_day(self):
        self.assertTrue(self.KIPass.get_customer_count_on_day(date="20220107").get("success"))

    def test_exception_get_customer_count_on_day(self):
        with self.assertRaises(ResponseIsNotSuccess):
            self.KIPass.get_customer_count_on_day(date="")

    def test_get_customer_count_on_two_week(self):
        self.assertTrue(self.KIPass.get_customer_count_on_two_week(start_date="20211219", end_date="20220102").get("success"))

    def test_exception_verify_qr(self):
        with self.assertRaises(ResponseIsNotSuccess):
            self.KIPass.verify_qr(parsed_qr_code="test_string")


if __name__ == "__main__":
    unittest.main()


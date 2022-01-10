class URLs:
    def __init__(self):
        self.base_url = "https://kipass.ssis.or.kr/kipassService/"

        self.login = "security/login"

        self.verify_qr = "verifySaveQR"

        self.customer_count_on_day = "security/passListTime"
        self.customer_count_on_two_week = "security/passCount2Week"

    def base_url(self):
        return self.base_url

    def login_url(self):
        return self.base_url + self.login

    def verify_qr_url(self):
        return self.base_url + self.verify_qr

    def customer_count_on_day_url(self):
        return self.base_url + self.customer_count_on_day

    def customer_count_on_two_week_url(self):
        return self.base_url + self.customer_count_on_two_week

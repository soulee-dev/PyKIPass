class RequestIsNotOkay(Exception):
    def __init__(self):
        super().__init__("Request is not okay")


class ResponseIsNotSuccess(Exception):
    def __init__(self):
        super().__init__("Response is not success")

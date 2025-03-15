from enum import Enum


class ResponseCode(Enum):
    SUCCESS = ("0", "成功")
    NO_DATA = ("1", "無資料")
    UNEXPECTED_ERROR = ("999", "預期外的錯誤")

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message

    def __str__(self):
        return f"{self.code} {self.message}"

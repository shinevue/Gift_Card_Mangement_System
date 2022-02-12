from enum import Enum


class ResponseStatus(Enum):
    OK = "ok"
    FAIL = "fail"


class AppEnvironment(Enum):
    PROD = "PROD"
    TEST = "TEST"

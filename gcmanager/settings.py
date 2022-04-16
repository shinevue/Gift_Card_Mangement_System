import os
from abc import ABC
from abc import abstractmethod
from typing import NewType
from typing import Type

from gcmanager.enums import AppEnvironment

Settings = NewType("Settings", dict)


class AppSettings(ABC):
    @staticmethod
    @abstractmethod
    def load() -> Settings:
        pass


class TestAppSettings(AppSettings):
    @staticmethod
    def load() -> Settings:
        return Settings(
            {
                "MONGODB_USERNAME": "testing_user",
                "MONGODB_PASSWORD": "testing",
                "MONGODB_HOST": "localhost",
                "MONGODB_PORT": "27020",
                "MONGODB_DBNAME": "testdb",
                "MONGODB_GC_COLLECTION_NAME": "testcollection",
            },
        )


class ProdAppSettings(AppSettings):
    @staticmethod
    def load() -> Settings:
        return Settings(
            {
                "MONGODB_USERNAME": os.environ.get("MONGODB_USERNAME"),
                "MONGODB_PASSWORD": os.environ.get("MONGODB_PASSWORD"),
                "MONGODB_HOST": os.environ.get("MONGODB_HOST"),
                "MONGODB_PORT": os.environ.get("MONGODB_PORT"),
                "MONGODB_DBNAME": os.environ.get("MONGODB_DBNAME", "gcmanager"),
                "MONGODB_GC_COLLECTION_NAME": os.environ.get(
                    "MONGODB_GC_COLLECTION_NAME",
                    "giftcards",
                ),
            },
        )


def settings_selector(enviroment: AppEnvironment) -> Type[AppSettings]:
    env_settings_map = {
        AppEnvironment.TEST: TestAppSettings,
        AppEnvironment.PROD: ProdAppSettings,
    }
    return env_settings_map[enviroment]

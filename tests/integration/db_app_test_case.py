import os

from falcon.testing import TestCase
from mockito import when
from pymongo import MongoClient

from gcmanager.app import create_app


class MongoDBAndAppAwareTestCase(TestCase):
    """
    A MongoDB and Falcon APP Aware Test Case
    use setUpExtended to set up items before executing
    your testcase
    """

    @classmethod
    def setUpClass(cls) -> None:
        when(os.environ).get("APP_ENV").thenReturn("TEST")
        cls.db_client = MongoClient(
            "mongodb://testing_user:testing@localhost:27020/",
            uuidRepresentation="standard",
        )
        cls.db_client.drop_database("testdb")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db_client.close()

    def setUp(self) -> None:
        super(MongoDBAndAppAwareTestCase, self).setUp()
        self.app = create_app()
        self.db = self.db_client["testdb"]
        self.collection = self.db["testcollection"]
        self.setUpExtended()

    def tearDown(self) -> None:
        self.collection.drop()
        self.db_client.drop_database(self.db)

    def setUpExtended(self) -> None:
        pass

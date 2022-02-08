import os

from falcon.testing import TestCase
from pymongo import MongoClient

from gcmanager.app import create_app


class MongoDBAndAppAwareTestCase(TestCase):
    """
    A MongoDB and Falcon APP Aware Test Case
    call super.setUp() before when using setup
    to set things up in your own testcase.
    """

    @classmethod
    def setUpClass(cls) -> None:
        os.environ["APP_ENV"] = "TEST"
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

    def tearDown(self) -> None:
        self.collection.drop()
        self.db_client.drop_database(self.db)

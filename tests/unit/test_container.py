import os
from unittest import TestCase

from kink.container import Container
from mockito import when

from gcmanager.dependencies import build_dependency_container
from gcmanager.exceptions import ImproperlyConfigured


class TestDependencyContainer(TestCase):
    def test_raises_exception_when_required_env_variables_absent(self) -> None:
        when(os.environ).get("APP_ENV").thenReturn("PROD")
        when(os.environ).get("MONGODB_USERNAME").thenReturn(None)
        when(os.environ).get("MONGODB_PASSWORD").thenReturn(None)
        when(os.environ).get("MONGODB_HOST").thenReturn(None)
        when(os.environ).get("MONGODB_PORT", "27017").thenReturn("27017")
        when(os.environ).get("MONGODB_DBNAME", "gcmanager").thenReturn("gcmanager")
        when(os.environ).get("MONGODB_GC_COLLECTION_NAME", "giftcards").thenReturn(
            "giftcards",
        )
        with self.assertRaises(ImproperlyConfigured):
            build_dependency_container()

    def test_returns_container_when_required_env_variables_present(self) -> None:
        when(os.environ).get("APP_ENV").thenReturn("PROD")
        when(os.environ).get("MONGODB_USERNAME").thenReturn("testing_user")
        when(os.environ).get("MONGODB_PASSWORD").thenReturn("testing")
        when(os.environ).get("MONGODB_HOST").thenReturn("localhost")
        when(os.environ).get("MONGODB_PORT", "27017").thenReturn("27020")
        when(os.environ).get("MONGODB_DBNAME", "gcmanager").thenReturn("testdb")
        when(os.environ).get("MONGODB_GC_COLLECTION_NAME", "giftcards").thenReturn(
            "testcollection",
        )
        self.assertIsInstance(build_dependency_container(), Container)

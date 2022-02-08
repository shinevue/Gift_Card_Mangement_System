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
        when(os.environ).get("MONGODB_PORT").thenReturn(None)
        when(os.environ).get("MONGODB_DBNAME").thenReturn(None)
        when(os.environ).get("MONGODB_GC_COLLECTION_NAME").thenReturn(None)
        with self.assertRaises(ImproperlyConfigured):
            build_dependency_container()

    def test_returns_container_when_required_env_variables_present(self) -> None:
        when(os.environ).get("APP_ENV").thenReturn("PROD")
        when(os.environ).get("MONGODB_USERNAME").thenReturn("someuser")
        when(os.environ).get("MONGODB_PASSWORD").thenReturn("somepassword")
        when(os.environ).get("MONGODB_HOST").thenReturn("somehost")
        when(os.environ).get("MONGODB_PORT").thenReturn(22222)
        when(os.environ).get("MONGODB_DBNAME").thenReturn("somedb")
        when(os.environ).get("MONGODB_GC_COLLECTION_NAME").thenReturn("somecollection")
        self.assertIsInstance(build_dependency_container(), Container)

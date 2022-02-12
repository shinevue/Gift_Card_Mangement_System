import os
from urllib.parse import quote

from kink import Container
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from gcmanager.enums import AppEnvironment
from gcmanager.exceptions import ImproperlyConfigured
from gcmanager.repositories import GiftCardMongoDBRepository
from gcmanager.settings import Settings
from gcmanager.settings import settings_selector
from gcmanager.usecases import AddGiftCardUseCase
from gcmanager.usecases import DenominationFetcherUseCase
from gcmanager.usecases import EditGiftCardUseCase
from gcmanager.usecases import FetchUnusedGiftCardsUseCase
from gcmanager.usecases import GiftCardAssetInformationUseCase
from gcmanager.usecases import MarkGiftCardUsedUseCase
from gcmanager.usecases import NearExpiryGiftCardFetcherUseCase
from gcmanager.webapi import DenominationResource
from gcmanager.webapi import GiftCardAssetInformationResource
from gcmanager.webapi import GiftCardResource
from gcmanager.webapi import MarkGiftCardUsedResource
from gcmanager.webapi import NearExpiryGiftCardResource


def _build_mongo_db_connection_string(container: Container) -> str:
    settings = container[Settings]
    username = settings.get("MONGODB_USERNAME")
    password = settings.get("MONGODB_PASSWORD")
    host = settings.get("MONGODB_HOST")
    port = settings.get("MONGODB_PORT")
    if not (username and password and host and port):
        raise ImproperlyConfigured(
            "environment variables required to "
            "build mongodb connection string are missing",
        )
    return "mongodb://%s:%s@%s:%s/" % (
        quote(username),
        quote(password),
        host,
        port,
    )


def _build_mongodb_client(container: Container) -> None:
    mongodb_connection_string = _build_mongo_db_connection_string(container)
    container[MongoClient] = lambda c: MongoClient(
        mongodb_connection_string,
        uuidRepresentation="standard",
    )


def _build_mongodb_database(container: Container) -> None:
    mongo_client = container[MongoClient]
    settings = container[Settings]
    container[Database] = lambda c: mongo_client[settings["MONGODB_DBNAME"]]


def _build_mongodb_collection(container: Container) -> None:
    database = container[Database]
    settings = container[Settings]
    container[Collection] = lambda c: database[settings["MONGODB_GC_COLLECTION_NAME"]]


def _build_mongodb_repository(container: Container) -> None:
    collection = container[Collection]
    container[GiftCardMongoDBRepository] = lambda c: GiftCardMongoDBRepository(
        collection,
    )


def _build_datasource_layer(container: Container) -> None:
    _build_mongodb_client(container)
    _build_mongodb_database(container)
    _build_mongodb_collection(container)
    _build_mongodb_repository(container)


def _build_use_cases(container: Container) -> None:
    repository = container[GiftCardMongoDBRepository]
    container[
        GiftCardAssetInformationUseCase
    ] = lambda c: GiftCardAssetInformationUseCase(repository)
    container[AddGiftCardUseCase] = lambda c: AddGiftCardUseCase(repository)
    container[DenominationFetcherUseCase] = lambda c: DenominationFetcherUseCase(
        repository,
    )
    container[
        NearExpiryGiftCardFetcherUseCase
    ] = lambda c: NearExpiryGiftCardFetcherUseCase(repository)
    container[MarkGiftCardUsedUseCase] = lambda c: MarkGiftCardUsedUseCase(repository)
    container[EditGiftCardUseCase] = lambda c: EditGiftCardUseCase(repository)
    container[FetchUnusedGiftCardsUseCase] = lambda c: FetchUnusedGiftCardsUseCase(
        repository,
    )


def _build_views(container: Container) -> None:
    gift_card_asset_use_case = container[GiftCardAssetInformationUseCase]
    container[
        GiftCardAssetInformationResource
    ] = lambda c: GiftCardAssetInformationResource(gift_card_asset_use_case)
    add_gc_use_case = container[AddGiftCardUseCase]
    fetch_unused_use_case = container[FetchUnusedGiftCardsUseCase]
    update_gc_use_case = container[EditGiftCardUseCase]
    container[GiftCardResource] = lambda c: GiftCardResource(
        add_gc_use_case,
        fetch_unused_use_case,
        update_gc_use_case,
    )
    denomination_fetcher_use_case = container[DenominationFetcherUseCase]
    container[DenominationResource] = lambda c: DenominationResource(
        denomination_fetcher_use_case,
    )
    near_expiry_gift_card_fetcher_use_case = container[NearExpiryGiftCardFetcherUseCase]
    container[NearExpiryGiftCardResource] = lambda c: NearExpiryGiftCardResource(
        near_expiry_gift_card_fetcher_use_case,
    )
    mark_gift_card_used_use_case = container[MarkGiftCardUsedUseCase]
    container[MarkGiftCardUsedResource] = lambda c: MarkGiftCardUsedResource(
        mark_gift_card_used_use_case,
    )


def build_dependency_container() -> Container:
    container = Container()
    app_environment = AppEnvironment(os.environ.get("APP_ENV"))
    settings_klass = settings_selector(app_environment)
    settings = settings_klass.load()
    container[Settings] = settings
    _build_datasource_layer(container)
    _build_use_cases(container)
    _build_views(container)
    return container

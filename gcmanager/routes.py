from falcon.routing import DefaultRouter
from falcon.routing import UUIDConverter
from kink import Container

from gcmanager.webapi import DenominationResource
from gcmanager.webapi import GiftCardAssetInformationResource
from gcmanager.webapi import GiftCardResource
from gcmanager.webapi import MarkGiftCardUsedResource
from gcmanager.webapi import NearExpiryGiftCardResource


def make_router(container: Container) -> DefaultRouter:
    router = DefaultRouter()
    router.options.converters.update({"giftcardid": UUIDConverter})
    router.add_route(
        "/api/giftcards/assets/",
        container[GiftCardAssetInformationResource],
    )
    router.add_route(
        "/api/giftcards/{gift_card_id:giftcardid}/mark-used/",
        container[MarkGiftCardUsedResource],
    )
    router.add_route(
        "/api/giftcards/denominations/",
        container[DenominationResource],
    )
    router.add_route(
        "/api/giftcards/denominations/{denomination:int(min=10, max=10000)}/",
        container[NearExpiryGiftCardResource],
    )
    router.add_route("/api/giftcards/", container[GiftCardResource])
    router.add_route(
        "/api/giftcards/{gift_card_id:giftcardid}/",
        container[GiftCardResource],
    )
    return router

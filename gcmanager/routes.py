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
    route_template_view_mapping = {
        "/api/giftcards/assets/": container[GiftCardAssetInformationResource],
        "/api/giftcards/{gift_card_id:giftcardid}/mark-used/": container[
            MarkGiftCardUsedResource
        ],
        "/api/giftcards/denominations/": container[DenominationResource],
        "/api/giftcards/denominations/{denomination:int(min=10, max=10000)}/": (
            container[NearExpiryGiftCardResource]
        ),
        "/api/giftcards/": container[GiftCardResource],
        "/api/giftcards/{gift_card_id:giftcardid}/": container[GiftCardResource],
    }
    for route_template, view in route_template_view_mapping.items():
        router.add_route(route_template, view)
    return router

import falcon
from falcon import App
from falcon.routing.converters import UUIDConverter

from gcmanager.dependencies import build_dependency_container
from gcmanager.webapi import DenominationResource
from gcmanager.webapi import GiftCardAssetInformationResource
from gcmanager.webapi import MarkGiftCardUsedResource
from gcmanager.webapi import NearExpiryGiftCardResource


def create_app() -> falcon.App:
    container = build_dependency_container()
    app = App()
    app.router_options.converters.update({"giftcardid": UUIDConverter})
    app.add_route(
        "/api/giftcards/assets/",
        container[GiftCardAssetInformationResource],
    )
    app.add_route(
        "/api/giftcards/{gift_card_id:giftcardid}/mark-used/",
        container[MarkGiftCardUsedResource],
    )
    app.add_route(
        "/api/giftcards/denominations/",
        container[DenominationResource],
    )
    app.add_route(
        "/api/giftcards/denominations/{denomination:int(min=10, max=10000)}/",
        container[NearExpiryGiftCardResource],
    )
    return app

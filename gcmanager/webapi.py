import json

import falcon

from gcmanager.usecases import GiftCardAssetInformationUseCase


class GiftCardAssetInformationResource:
    def __init__(self, use_case: GiftCardAssetInformationUseCase) -> None:
        self._use_case = use_case

    def on_get(self, request: falcon.Request, response: falcon.Response) -> None:
        assets = self._use_case.summarize()
        response.text = json.dumps(
            {
                "status": "ok",
                "data": {
                    "total": assets.total,
                    "used": assets.used,
                    "unused": assets.unused,
                },
            },
        )

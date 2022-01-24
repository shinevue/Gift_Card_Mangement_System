import falcon

from gcmanager.domain import SuccessfulResponse
from gcmanager.serializers import GiftCardAssetSummarySerializer
from gcmanager.usecases import GiftCardAssetInformationUseCase


class GiftCardAssetInformationResource:
    def __init__(self, use_case: GiftCardAssetInformationUseCase) -> None:
        self._use_case = use_case
        self._serializer = GiftCardAssetSummarySerializer()

    def on_get(self, request: falcon.Request, response: falcon.Response) -> None:
        assets = self._use_case.summarize()
        serialized_data = self._serializer.dump(assets)
        response.text = SuccessfulResponse(data=serialized_data).serialize()
        response.status = falcon.HTTP_200

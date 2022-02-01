import json

import falcon
from falcon import errors
from marshmallow import ValidationError

from gcmanager.domain import Denomination
from gcmanager.domain import GiftCardID
from gcmanager.domain import SuccessfulResponse
from gcmanager.exceptions import GiftCardAlreadyExists
from gcmanager.exceptions import GiftCardAlreadyUsed
from gcmanager.exceptions import GiftCardNotFound
from gcmanager.exceptions import GiftCardNotFoundForDenomination
from gcmanager.serializers import GiftCardAssetSummarySerializer
from gcmanager.serializers import GiftCardCreateRequestSerializer
from gcmanager.serializers import GiftCardSerializer
from gcmanager.serializers import GiftCardUpdateRequestSerializer
from gcmanager.usecases import AddGiftCardUseCase
from gcmanager.usecases import DenominationFetcherUseCase
from gcmanager.usecases import EditGiftCardUseCase
from gcmanager.usecases import FetchUnusedGiftCardsUseCase
from gcmanager.usecases import GiftCardAssetInformationUseCase
from gcmanager.usecases import MarkGiftCardUsedUseCase
from gcmanager.usecases import NearExpiryGiftCardFetcherUseCase


class GiftCardAssetInformationResource:
    def __init__(self, use_case: GiftCardAssetInformationUseCase) -> None:
        self._use_case = use_case
        self._serializer = GiftCardAssetSummarySerializer()

    def on_get(self, request: falcon.Request, response: falcon.Response) -> None:
        assets = self._use_case.summarize()
        serialized_data = self._serializer.dump(assets)
        response.text = SuccessfulResponse(data=serialized_data).serialize()
        response.status = falcon.HTTP_200


class GiftCardResource:
    def __init__(
        self,
        create_use_case: AddGiftCardUseCase,
        get_unused_use_case: FetchUnusedGiftCardsUseCase,
        update_use_case: EditGiftCardUseCase,
    ) -> None:
        self._create_use_case = create_use_case
        self._get_unused_use_case = get_unused_use_case
        self._update_use_case = update_use_case
        self._dump_serializer = GiftCardSerializer()
        self._create_serializer = GiftCardCreateRequestSerializer()
        self._update_serializer = GiftCardUpdateRequestSerializer()

    def on_get(self, request: falcon.Request, response: falcon.Response) -> None:
        gift_cards = self._get_unused_use_case.fetch()
        serialized_data = self._dump_serializer.dump(gift_cards, many=True)
        response.text = SuccessfulResponse(data=serialized_data).serialize()
        response.status = falcon.HTTP_200

    def on_post(self, request: falcon.Request, response: falcon.Response) -> None:
        payload = json.loads(request.bounded_stream.read())
        try:
            gift_card_create_request = self._create_serializer.load(payload)
        except ValidationError as validation_error:
            raise errors.HTTPBadRequest(
                title="Validation Error",
                description=validation_error.messages,
            )
        try:
            self._create_use_case.create(gift_card_create_request)
        except GiftCardAlreadyExists:
            raise errors.HTTPBadRequest
        response.status = falcon.HTTP_201

    def on_put(
        self,
        request: falcon.Request,
        response: falcon.Response,
        gift_card_id: GiftCardID,
    ) -> None:
        payload = json.loads(request.bounded_stream.read())
        try:
            update_request = self._update_serializer.load(
                {"id": gift_card_id, **payload},
            )
        except ValidationError:
            raise errors.HTTPBadRequest
        try:
            self._update_use_case.edit_gc(update_request)
        except GiftCardNotFound:
            raise errors.HTTPNotFound
        except GiftCardAlreadyUsed:
            raise errors.HTTPBadRequest
        response.status = falcon.HTTP_200


class DenominationResource:
    def __init__(self, use_case: DenominationFetcherUseCase) -> None:
        self._use_case = use_case

    def on_get(self, request: falcon.Request, response: falcon.Response) -> None:
        denominations = self._use_case.fetch()
        response.status = falcon.HTTP_200
        response.text = SuccessfulResponse(denominations).serialize()


class NearExpiryGiftCardResource:
    def __init__(self, use_case: NearExpiryGiftCardFetcherUseCase) -> None:
        self._use_case = use_case
        self._serializer = GiftCardSerializer()

    def on_get(
        self,
        request: falcon.Request,
        response: falcon.Response,
        denomination: int,
    ) -> None:
        try:
            gift_card = self._use_case.fetch(Denomination(denomination))
        except GiftCardNotFoundForDenomination:
            raise errors.HTTPNotFound
        serialized_data = self._serializer.dump(gift_card)
        response.status = falcon.HTTP_200
        response.text = SuccessfulResponse(serialized_data).serialize()


class MarkGiftCardUsedResource:
    def __init__(self, use_case: MarkGiftCardUsedUseCase) -> None:
        self._use_case = use_case

    def on_post(
        self,
        request: falcon.Request,
        response: falcon.Response,
        gift_card_id: GiftCardID,
    ) -> None:
        try:
            self._use_case.mark_used(gift_card_id)
        except GiftCardNotFound:
            raise errors.HTTPBadRequest
        response.status = falcon.HTTP_200

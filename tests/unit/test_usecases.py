from unittest import TestCase
from unittest.mock import Mock

from gcmanager.usecases import GiftCardUseCase


class TestGiftCardUseCase(TestCase):
    def setUp(self) -> None:
        self.gift_card_repository = Mock()

    def test_gift_card_accepts_repository(self) -> None:
        GiftCardUseCase(self.gift_card_repository)

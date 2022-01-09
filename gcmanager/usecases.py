from gcmanager.repositories import GiftCardRepository


class GiftCardUseCase:
    def __init__(self, gift_card_repository: GiftCardRepository) -> None:
        self.gift_card_repository = gift_card_repository

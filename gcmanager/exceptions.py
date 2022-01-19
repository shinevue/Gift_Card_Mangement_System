class GiftCardAlreadyExists(Exception):
    pass


class GiftCardNotFound(Exception):
    pass


class GiftCardNotFoundForDenomination(GiftCardNotFound):
    pass


class GiftCardAlreadyUsed(Exception):
    pass

from datetime import date

from marshmallow.validate import ValidationError


def date_not_more_than_equal_to_a_year_old(dt: date) -> date:
    today = date.today()
    if dt <= today.replace(year=today.year - 1):
        raise ValidationError("Date of issue cannot be more than or a year old")
    return dt

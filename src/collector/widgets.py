from django import forms


class DatePickerFieldWidget(forms.DateInput):
    """."""

    input_type = "date"

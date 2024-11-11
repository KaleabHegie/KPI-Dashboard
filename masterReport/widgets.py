from django.forms.widgets import DateTimeInput

class DateTimeInputWidget(DateTimeInput):
    input_type = 'datetime-local'
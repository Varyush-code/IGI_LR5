from django import forms
from .models import Ticket
from .models import PromoCode

class TicketForm(forms.ModelForm):

    promocode = forms.ModelChoiceField(
        queryset=PromoCode.objects.filter(active=True),
        required=False
    )

    class Meta:

        model = Ticket

        fields = [
            'day_type',
            'feeding_show',
            'active_hours',
            'promocode'
        ]

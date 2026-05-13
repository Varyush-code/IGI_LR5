from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from datetime import date

class RegisterForm(UserCreationForm):

    birth_date = forms.DateField(label='дата рождения', widget = forms.DateInput(attrs={"type": "data"}))

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'birth_date',
            'password1',
            'password2'
        ]

    def clean_age(self):
        db = self.cleaned_data["birth_date"]
        today = date.today()

        age = today.year - db.year - (
            (today.month, today.day) < (db.month, db.day)
        )
        if age < 18:
            raise forms.ValidationError("Только 18+")
        return age
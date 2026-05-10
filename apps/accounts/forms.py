from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):

    age = forms.IntegerField(label='Возраст')

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'age',
            'password1',
            'password2'
        ]

    def clean_age(self):

        age = self.cleaned_data['age']
        if age < 18:
            raise forms.ValidationError('Мы малолеток не пускаем')
        return age
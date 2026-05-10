from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm
from .models import Profile

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        profile = self.object.profile
        profile.age = form.cleaned_data['age']
        profile.full_clean()
        profile.save()
        return response
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from .models import User
from .forms import ParentSignUpForm


class ParentSignUpView(CreateView):
    model = User
    form_class = ParentSignUpForm
    template_name = 'templates/main/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'parent'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main:child_stats')

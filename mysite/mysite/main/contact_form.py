from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from .models import Contact_Message
from .forms import ContactForm


class ContactFormView(CreateView):
    model = Contact_Message
    form_class = ContactForm
    template_name = 'templates/main/contact_us.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'parent'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        contact_message = form.save()
        return redirect('/welcome')

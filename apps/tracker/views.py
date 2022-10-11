from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView


class HomePageView(TemplateView):
    # Specify template name to use app level home.html.
    template_name = "app-tracker/home.html"


class SignUpView(CreateView):
    # Use Django's generic Creation form for the signup.
    form_class = UserCreationForm
    # Redirect the user to the login page after signing up successfully.
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

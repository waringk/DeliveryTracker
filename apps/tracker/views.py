from .forms import UserRegisterForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView


class HomePageView(TemplateView):
    # Specify template name to use app level home.html.
    template_name = "app-tracker/home.html"


class SignUpView(CreateView):
    # Use UserRegisterForm for the signup view.
    form_class = UserRegisterForm
    # Redirect the user to the login page after signing up successfully.
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

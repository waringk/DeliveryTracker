from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    # Specify template name to use app level home.html
    template_name = "app-tracker/home.html"

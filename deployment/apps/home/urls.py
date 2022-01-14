# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [

    path('about/', TemplateView.as_view(template_name="about.html")),

    # The home page
    path('', views.index, name='home'),

    path('states/', views.states, name='states'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]

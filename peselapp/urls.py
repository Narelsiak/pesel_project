from django.urls import path
from . import views

urlpatterns = [
    path("", views.pesel_view, name="pesel_view"),
]

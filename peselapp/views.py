# views.py
from django.shortcuts import render
from .forms import PeselForm

def pesel_view(request):
    form = PeselForm()
    return render(request, "pesel.html", {"form": form})

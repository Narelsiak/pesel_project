# views.py
from django.shortcuts import render, redirect
from .forms import PeselForm
from django.http import HttpRequest, HttpResponse
from typing import Optional
from .utils import validate_pesel

def pesel_view(request: HttpRequest) -> HttpResponse:

    result: dict[str, Optional[str] | bool]
    if request.method == "POST":
        form = PeselForm(request.POST)
        if form.is_valid():
            pesel: str = form.cleaned_data["pesel"]
            result = validate_pesel(pesel)

            request.session['pesel_result'] = result
            print(result)
            return redirect('pesel_view')  # Redirect to GET to avoid resubmission
    else:
        form = PeselForm()
        result = request.session.pop('pesel_result', None)
    
    return render(request, "pesel.html", {"form": form})

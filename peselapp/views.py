# views.py
from django.shortcuts import render, redirect
from .forms import PeselForm
from django.http import HttpRequest, HttpResponse
from typing import Optional, Dict, Any
from .utils import validate_pesel

def pesel_view(request: HttpRequest) -> HttpResponse:
    """
    Handles PESEL validation form submission and displays the result.

    GET request:
        - Renders the form
        - If a previous result is stored in the session, retrieves and removes it

    POST request:
        - Validates the submitted form
        - Checks the PESEL number using `validate_pesel`
        - Stores the result in the session and redirects to GET to display it

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: Rendered page with the form and optional validation result
    """
    result: Optional[Dict[str, Any]] = None

    if request.method == "POST":
        form = PeselForm(request.POST)
        if form.is_valid():
            pesel: str = form.cleaned_data["pesel"]
            result = validate_pesel(pesel)

            request.session['pesel_result'] = result
            return redirect('pesel_view')  # Redirect to GET to avoid resubmission
    else:
        form = PeselForm()
        result = request.session.pop('pesel_result', None)
    
    return render(request, "pesel.html", {"form": form, "result": result})

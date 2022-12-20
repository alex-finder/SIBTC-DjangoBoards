from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, redirect

from .forms import SignUpForm


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        # The initial code was: form = UserCreationForm()
        # this is causing the unittest to fail
        # TODO: potential test case training
        # form = UserCreationForm()
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

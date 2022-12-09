from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import Board


def home(request: HttpRequest) -> HttpResponse:
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, HttpResponse
# Create your views here.


def main_page_view(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name='main-page.html'
    )


def appeals(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name='appeals.html'
    )


def appeal(request: HttpRequest, pk: int) -> HttpResponse:
    return render(
        request=request,
        template_name='appeal.html'
    )


def sign_in(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect(to=reverse(viewname='frontend:main-page'))
    return render(
        request=request,
        template_name='sign-in.html'
    )


def sign_up(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect(to=reverse(viewname='frontend:main-page'))
    return render(
        request=request,
        template_name='sign-up.html'
    )


def sign_out(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name='sign-out.html'
    )


def dashboard(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name='dashboard.html'
    )
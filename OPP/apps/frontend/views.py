from django.shortcuts import render, redirect, reverse
from django.http import HttpRequest, HttpResponse

from apps.api.utils import general
from apps.api import models
from apps.api.utils import decorators
# Create your views here.


def main_page_view(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name='main-page.html'
    )


@decorators.check_authorized_decorator
def appeals(request: HttpRequest) -> HttpResponse:
    role = general.get_role_by_user(user=request.user)  # type: ignore
    if role != 'engineer':
        return HttpResponse(status=404)

    return render(request=request, template_name='appeals.html')


@decorators.check_authorized_decorator
def dashboard(request: HttpRequest) -> HttpResponse:
    augmented_user = models.Engineer.objects.filter(user=request.user).first()  # type: ignore
    if augmented_user is not None:
        role = 'engineer'
    else:
        role = 'manager'

    return render(
        request=request,
        template_name='dashboard.html',
        context={'role': role}
    )


def sign_in(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:  # type: ignore
        return redirect(to=reverse(viewname='frontend:main-page'))
    return render(
        request=request,
        template_name='sign-in.html'
    )


def sign_out(request: HttpRequest) -> HttpResponse:
    return render(
        request=request,
        template_name='sign-out.html'
    )
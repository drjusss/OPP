from django.urls import path
from apps.frontend import views

app_name = 'frontend'

urlpatterns = [
    path(route='', view=views.main_page_view, name='main-page'),
    path(route='auth/sign-in/', view=views.sign_in, name='sign-in'),
    path(route='auth/sign-up/', view=views.sign_up, name='sign-up'),
    path(route='auth/sign-out/', view=views.sign_out, name='sign-out'),
    path(route='appeals', view=views.appeals, name='appeals'),
    path(route='appeal/<int:pk>/', view=views.appeal, name='appeal')
]
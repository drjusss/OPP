from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    path('appeals/', views.AppealsApiView.as_view(), name='appeals'),
    path('appeal/<pk:int>/', views.AppealApiView.as_view(), name='appeal'),
]
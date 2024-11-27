from django.urls import path
from apps.api.views.model import appeal
from apps.api.views import authorization

app_name = 'api'

urlpatterns = [
    path('appeals/', appeal.AppealsApiView.as_view(), name='appeals'),  # Для класса BasedView необходимо добавлять as_view,
    path('appeal/<int:pk>/', appeal.AppealApiView.as_view(), name='appeal'),
    path('fixiks/', appeal.FixiksApiView.as_view(), name='fixiks'),


    path(route='auth/sign-up/', view=authorization.SignUpApiView.as_view(), name='sign_up'),
    path(route='auth/sign-in/', view=authorization.SignInApiView.as_view(), name='sign-in'),
    path(route='auth/sign-out/', view=authorization.SignOutApiView.as_view(), name='sign-out'),
]

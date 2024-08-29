from .views import SignUpView, UserView, UpdateProfileView
from django.urls import path, include

urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
    path('user/', UserView.as_view()),
    path('update-profile/', UpdateProfileView, name='update-profile'),
]

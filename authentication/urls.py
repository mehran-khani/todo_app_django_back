from django.urls import path
from .views import RegisterView, VerifyEmailView

urlpatterns = [
    path("", RegisterView.as_view()),
    path("verify-email/", VerifyEmailView.as_view()),
]

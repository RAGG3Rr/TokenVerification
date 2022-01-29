from django.urls import path
from .views import RegisterView, LoginView, verify_email

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('verify/<uidb64>/<token>', verify_email, name='verify')
]
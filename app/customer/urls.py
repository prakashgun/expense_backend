from django.urls import path

from .views import RegisterView, VerifyRegisterView

app_name = 'customer'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-register/', VerifyRegisterView.as_view(), name='verify-register'),
    path('login/', RegisterView.as_view(), name='login')
]

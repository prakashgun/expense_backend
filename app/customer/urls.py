from django.urls import path

from .views import RegisterView, VerifyRegisterView, LoginView, VerifyLoginView, LogoutView

app_name = 'customer'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-register/', VerifyRegisterView.as_view(), name='verify-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-login/', VerifyLoginView.as_view(), name='verify-login'),
    path('logout/', LogoutView.as_view(), name='logout')
]

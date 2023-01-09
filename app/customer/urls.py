from django.urls import path

from .views import Register

app_name = 'customer'

urlpatterns = [
    path('register/', Register.as_view(), name='register')
]

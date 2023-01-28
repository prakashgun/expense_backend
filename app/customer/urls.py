from django.urls import path

from .views import UserPhoneView

app_name = 'customer'

urlpatterns = [
    path('user-phone/', UserPhoneView.as_view(), name='phone')
]

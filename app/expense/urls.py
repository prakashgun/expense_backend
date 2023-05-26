from django.urls import path

from .views import AccountList, AccountDetail, CategoryList, CategoryDetail

app_name = 'expense'

urlpatterns = [
    path('accounts/', AccountList.as_view(), name='account-list'),
    path('accounts/<pk>', AccountDetail.as_view(), name='account-detail'),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<pk>', CategoryDetail.as_view(), name='category-detail')
]

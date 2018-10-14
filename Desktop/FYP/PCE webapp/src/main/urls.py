from django.urls import path, re_path, include
from .views import (
    home,
    allproducts,
    search
)

urlpatterns = [
    path('', home, name='home'),
    path('allproducts', allproducts, name='allproducts'),
    path('search/<str:query>/', search, name='search' )
]

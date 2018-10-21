from django.urls import path, re_path, include
from .views import (
    home,
    search,
    product
)

urlpatterns = [
    path('', home, name='home'),
    path('search/<str:query>/', search, name='search' ),
    re_path(r'^item/(?:(?P<id>[\d\-]+)/)?$', product, name='product'),
]

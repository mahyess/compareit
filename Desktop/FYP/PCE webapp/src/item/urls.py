
from django.contrib import admin
from django.urls import path, re_path, include
from .views import (item)

urlpatterns = [
# path('', home, name='home'),
     re_path(r'^(?P<id>\d+)/$',item, name='item'),
]

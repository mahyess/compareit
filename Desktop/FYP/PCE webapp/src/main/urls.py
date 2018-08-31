from django.urls import path, re_path, include
from .views import (
    home,
)

urlpatterns = [
    path('', home, name='home'),
]

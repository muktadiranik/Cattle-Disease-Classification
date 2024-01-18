from django.urls import path
from diseases.views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
]

from django.urls import path
from diseases.views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("api/", IndexAPIView.as_view(), name="api"),
    path("diseases/", DiseaseAPIView.as_view(), name="diseases"),
]

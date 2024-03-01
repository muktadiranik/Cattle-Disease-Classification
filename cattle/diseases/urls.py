from django.urls import path
from django.views.generic import TemplateView
from diseases.views import *

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("about/", IndexView.as_view(), name="about"),
    path("api/", IndexAPIView.as_view(), name="api"),
    path("diseases/", DiseaseAPIView.as_view(), name="diseases"),
]

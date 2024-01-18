from django.shortcuts import render
from django.views import View
from diseases.forms import *


class IndexView(View):
    def get(self, request):
        form = CattleImageAndDiseaseDescriptionForm()
        return render(request, "diseases/index.html", {
            "form": form
        })

    def post(self, request):
        form = CattleImageAndDiseaseDescriptionForm(
            request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return render(request, "diseases/index.html", {
            "form": form
        })

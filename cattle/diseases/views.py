from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render
from django.views import View
from diseases.forms import CattleImageAndDiseaseDescriptionForm
from diseases.models import CattleImageAndDiseaseDescription
from diseases.utils import compare_images


class IndexView(View):
    def get(self, request):
        form = CattleImageAndDiseaseDescriptionForm()
        return render(request, "diseases/index.html", {"form": form})

    def post(self, request):
        form = CattleImageAndDiseaseDescriptionForm(
            request.POST, request.FILES)

        if form.is_valid():
            for i in CattleImageAndDiseaseDescription.objects.all():
                image_front = i.image_front
                image_back = i.image_back
                image_left = i.image_left
                image_right = i.image_right

                if (
                    compare_images(image_front, form.cleaned_data["image_front"]) or
                    compare_images(image_front, form.cleaned_data["image_back"]) or
                    compare_images(image_front, form.cleaned_data["image_left"]) or
                    compare_images(
                        image_front, form.cleaned_data["image_right"])
                ) or (
                    compare_images(image_back, form.cleaned_data["image_front"]) or
                    compare_images(image_back, form.cleaned_data["image_back"]) or
                    compare_images(image_back, form.cleaned_data["image_left"]) or
                    compare_images(
                        image_back, form.cleaned_data["image_right"])
                ) or (
                    compare_images(image_left, form.cleaned_data["image_front"]) or
                    compare_images(image_left, form.cleaned_data["image_back"]) or
                    compare_images(image_left, form.cleaned_data["image_left"]) or
                    compare_images(
                        image_left, form.cleaned_data["image_right"])
                ) or (
                    compare_images(image_right, form.cleaned_data["image_front"]) or
                    compare_images(image_right, form.cleaned_data["image_back"]) or
                    compare_images(image_right, form.cleaned_data["image_left"]) or
                    compare_images(
                        image_right, form.cleaned_data["image_right"])
                ):
                    messages.error(request, "Image matches an existing image.")
                    return render(request, "diseases/index.html", {"form": form})

            form.save()
            messages.success(request, "Image successfully saved.")

        return render(request, "diseases/index.html", {"form": form})

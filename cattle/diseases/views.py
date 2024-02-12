from django.db.transaction import atomic
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render
from django.views import View
from diseases.forms import *
from diseases.models import *
from diseases.serializers import *
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


class IndexAPIView(APIView):
    def post(self, request):
        with atomic():
            cattle_disease_description = CattleDiseaseDescription.objects.create(
                user_phone=request.data.get("user_phone"),
                description=request.data.get("description"),
                doctor_advice=request.data.get("doctor_advice"),
                diagonosis=request.data.get("diagonosis"),
                treatment=request.data.get("treatment"),
                disease=CattleDisease.objects.get(
                    id=request.data.get("disease")),
                approved=False
            )

            for i in request.FILES.getlist("images"):
                count = CattleDiseaseImage.objects.all().count()

                for j in CattleDiseaseImage.objects.all():
                    if compare_images(i, j.cattle_image):
                        return Response({"data": "Image matches an existing image"}, status=status.HTTP_400_BAD_REQUEST)

                custom_image = default_storage.save(
                    f"images/{cattle_disease_description.disease.code_name}_{count + 1}.png", i)

                CattleDiseaseImage.objects.create(
                    cattle_disease_description=cattle_disease_description,
                    cattle_image=custom_image
                )

            return Response({"data": "Image successfully saved"}, status=status.HTTP_201_CREATED)


class DiseaseAPIView(APIView):
    def get(self, request):
        cattle_disease = CattleDisease.objects.all()
        serializer = CattleDiseaseSerializer(cattle_disease, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

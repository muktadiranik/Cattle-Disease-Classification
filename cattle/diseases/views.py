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
            user_phone = request.data.get("user_phone")
            description = request.data.get("description")
            doctor_advice = request.data.get("doctor_advice")
            diagonosis = request.data.get("diagonosis")
            treatment = request.data.get("treatment")
            disease_id = request.data.get("disease")

            disease = CattleDisease.objects.get(id=disease_id)

            cattle_disease_description = CattleDiseaseDescription.objects.create(
                user_phone=user_phone,
                description=description,
                doctor_advice=doctor_advice,
                diagonosis=diagonosis,
                treatment=treatment,
                disease=disease,
                approved=False
            )

            for i, image in enumerate(request.data.getlist("images"), start=1):
                count = CattleDiseaseImage.objects.filter(
                    cattle_disease_description__disease=disease).count()

                for existing_image in CattleDiseaseImage.objects.filter(cattle_disease_description__disease=disease):
                    if compare_images(image, existing_image.cattle_image):
                        return Response({"data": "Image matches an existing image"}, status=status.HTTP_400_BAD_REQUEST)

                custom_image_name = f"{disease.code_name}_{count + 1}.png"
                custom_image = default_storage.save(
                    f"images/{custom_image_name}", image)

                CattleDiseaseImage.objects.create(
                    cattle_disease_description=cattle_disease_description,
                    cattle_image=custom_image
                )

            return Response({"data": "Images successfully saved"}, status=status.HTTP_201_CREATED)


class DiseaseAPIView(APIView):
    def get(self, request):
        cattle_disease = CattleDisease.objects.all()
        serializer = CattleDiseaseSerializer(cattle_disease, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
